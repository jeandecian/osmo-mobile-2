import asyncio

from bleak import BleakScanner
from bleak.backends.device import BLEDevice


class Bluetooth:
    """Handles low-level BLE scanning and device discovery."""

    def __init__(self, timeout: float = 5.0) -> None:
        self.timeout: float = timeout

    async def scan(self) -> list[BLEDevice]:
        """Scans for nearby BLE devices and returns discovered devices."""

        return await BleakScanner.discover(timeout=self.timeout)


def find_target_device(devices: list[BLEDevice]) -> BLEDevice | None:
    """Finds a target device from a list of BLE devices."""

    for device in devices:
        device_name: str = (device.name or "").lower()

        if "dji" in device_name or "osmo" in device_name:
            return device

    return None


async def main() -> None:
    bt: Bluetooth = Bluetooth()

    print("Scanning for BLE devices...")
    devices: list[BLEDevice] = await bt.scan()
    target_device: BLEDevice | None = find_target_device(devices)

    if not target_device:
        print("No target device found.")
        return

    print(f"Found target device: {target_device}")


if __name__ == "__main__":
    asyncio.run(main())
