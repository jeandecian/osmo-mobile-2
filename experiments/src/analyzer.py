import sys
from collections import defaultdict
from pathlib import Path


class Analyzer:
    """Ingests capture log files and manages raw payload data for analysis."""

    def __init__(self, log_path: str | Path) -> None:
        self.log_path: Path = Path(log_path)
        self.payloads: list[bytes] = []
        self.frames: list[bytes] = []

    def load_payloads(self) -> list[bytes]:
        """Reads the log file line-by-line and extracts raw hex bytes."""

        if not self.log_path.exists():
            raise FileNotFoundError(f"Capture file not found: {self.log_path}")

        payloads: list[bytes] = []

        with open(self.log_path, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line or "|" not in line:
                    continue

                hex_str: str = line.rsplit("|", 1)[-1].strip()

                try:
                    payloads.append(bytes.fromhex(hex_str))
                except ValueError:
                    print(
                        f"[Warning] Line {line_num}: Skipping invalid hex string '{hex_str}'"
                    )

        self.payloads = payloads

        return self.payloads

    def reassemble_frames(self) -> list[bytes]:
        """Reassembles fragmented BLE payloads into complete frames based on the 20-byte MTU limit."""

        frames: list[bytes] = []
        buffer: bytearray = bytearray()

        for payload in self.payloads:
            buffer.extend(payload)

            if len(payload) < 20:
                frames.append(bytes(buffer))
                buffer.clear()

        if buffer:
            frames.append(bytes(buffer))

        self.frames = frames

        return self.frames


def print_head_tail(
    items: list[bytes], label: str = "Items", head: int = 5, tail: int = 5
) -> None:
    """Prints the head and tail of a list of bytes with index formatting."""

    total: int = len(items)
    index_width: int = len(str(total))

    max_length: int = max(len(item) for item in items)
    length_width: int = len(str(max_length))

    print("-" * 64)
    print(f"{label} (Total: {total})")
    print("-" * 64)

    if total <= head + tail:
        for idx, item in enumerate(items):
            print(
                f"{idx:>{index_width}} | {len(item):>{length_width}} | {item.hex(' ')}"
            )
    else:
        for idx in range(head):
            item = items[idx]
            print(
                f"{idx:>{index_width}} | {len(item):>{length_width}} | {item.hex(' ')}"
            )

        print(
            f"{'-' * index_width} | {'-' * length_width} | -- {total - (head + tail)} {label.lower()} omitted --"
        )

        for idx in range(total - tail, total):
            item = items[idx]
            print(
                f"{idx:>{index_width}} | {len(item):>{length_width}} | {item.hex(' ')}"
            )

    print("-" * 64)


def get_unique_lengths(items: list[bytes], label: str = "Items") -> list[int]:
    """Returns a sorted list of unique byte lengths present in the dataset."""

    unique_lengths: list[int] = sorted({len(item) for item in items})

    print(
        f"Unique {label.capitalize()} Lengths (bytes):",
        ", ".join(str(length) for length in unique_lengths),
    )
    print("-" * 64)

    return unique_lengths


def _find_variant_ranges(
    length: int, identical_indices: set[int]
) -> list[tuple[int, int]]:
    """Identifies contiguous byte indices that contain variations across frames."""

    variant_ranges: list[tuple[int, int]] = []

    i = 0
    while i < length:
        if i not in identical_indices:
            start = i
            while i < length and i not in identical_indices:
                i += 1

            variant_ranges.append((start, i))
        else:
            i += 1

    return variant_ranges


def _infer_field_type(var_pct: float) -> str:
    """Classifies a byte field based on its variation ratio."""

    if var_pct > 50.0:
        return "Sensor/Counter"

    if var_pct > 5.0:
        return "State/Dynamic"

    return "Config/Enum"


def _format_range_str(start: int, end: int) -> str:
    """Formats byte index or range into a standardized display label."""

    return f"Byte {start}" if start == end - 1 else f"Byte {start}-{end - 1}"


def _print_variant_row(
    start: int, end: int, raw_group: list[bytes], total_frames: int
) -> None:
    """Calculates statistics and prints a single variant range row."""

    range_str: str = _format_range_str(start, end)
    variants: list[str] = sorted({f[start:end].hex(" ") for f in raw_group})
    num_vars: int = len(variants)
    var_pct: float = (num_vars / total_frames) * 100
    field_type: str = _infer_field_type(var_pct)

    vals_str: str = ", ".join(f"[{v}]" for v in variants[: min(5, num_vars)])
    if num_vars > 5:
        vals_str += f", (+{num_vars - 5} more)"

    print(
        f"{range_str:<10} | {num_vars:>10} | {var_pct:>11.1f} | {field_type:<14} | {vals_str}"
    )


def _analyze_single_length_group(length: int, raw_group: list[bytes]) -> None:
    """Analyzes layout and variations for frames of a specific byte length."""

    total_frames: int = len(raw_group)
    unique_group: list[bytes] = list(dict.fromkeys(raw_group))

    print(
        f"\n--- Length: {length} bytes ({len(unique_group)} unique frame(s) out of {total_frames} total) ---"
    )

    if len(unique_group) == 1:
        print(f"Frame: {unique_group[0].hex(' ')}")
        print("No variants detected (single unique sample captured).")
        return

    identical_indices: set[int] = {
        i for i in range(length) if len({f[i] for f in unique_group}) == 1
    }

    template_tokens: list[str] = [
        f"{unique_group[0][i]:02x}" if i in identical_indices else f"[Byte {i}]"
        for i in range(length)
    ]
    print(f"Frame Layout: {' '.join(template_tokens)}")

    variant_ranges: list[tuple[int, int]] = _find_variant_ranges(
        length, identical_indices
    )

    print(
        f"{'Byte Range':<10} | Variations | % Var/Total | {'Inferred Type':<14} | {'Unique Value(s)'}"
    )
    print(f"{'-'*10}-+-{'-'*10}-+-{'-'*11}-+-{'-'*14}-+-{'-'*19}")

    for start, end in variant_ranges:
        _print_variant_row(start, end, raw_group, total_frames)


def analyze_frame_patterns(frames: list[bytes]) -> None:
    """Groups frames by length and delegates pattern analysis."""

    raw_frames_by_len: dict[int, list[bytes]] = defaultdict(list)

    for frame in frames:
        raw_frames_by_len[len(frame)].append(frame)

    for length in sorted(raw_frames_by_len.keys()):
        _analyze_single_length_group(length, raw_frames_by_len[length])


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 analyzer.py <path_to_capture_log>")
        sys.exit(1)

    analyzer: Analyzer = Analyzer(Path(sys.argv[1]))

    payloads: list[bytes] = analyzer.load_payloads()
    print_head_tail(payloads, label="Payloads")

    payload_lengths: list[int] = get_unique_lengths(payloads, label="Payload")
    if payload_lengths:
        print(
            f"\n[NOTE] Maximum observed payload length: {max(payload_lengths)} bytes."
        )
        print(
            "[NOTE] Captures are capped at 20 bytes due to the standard BLE ATT MTU limit "
            "(23-byte default MTU minus 3 bytes of ATT protocol overhead)."
        )
        print(
            "[NOTE] Frames larger than 20 bytes are split across multiple consecutive payloads "
            "and must be reassembled into a single stream."
        )
        print()

    frames: list[bytes] = analyzer.reassemble_frames()
    print_head_tail(frames, label="Frames")
    get_unique_lengths(frames, label="Frame")

    analyze_frame_patterns(frames)


if __name__ == "__main__":
    main()
