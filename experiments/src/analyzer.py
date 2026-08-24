import sys
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


if __name__ == "__main__":
    main()
