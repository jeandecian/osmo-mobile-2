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


async def main() -> None:
    bt: Bluetooth = Bluetooth()

    print("Scanning for BLE devices...")
    devices: list[BLEDevice] = await bt.scan()

    for device in devices:
        print(device)


if __name__ == "__main__":
    asyncio.run(main())
