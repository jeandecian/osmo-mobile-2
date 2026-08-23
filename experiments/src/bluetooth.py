import asyncio

from bleak import BleakClient, BleakScanner
from bleak.backends.device import BLEDevice
from bleak.exc import BleakError


class Bluetooth:
    """Handles low-level BLE scanning and connection management."""

    def __init__(self, timeout: float = 5.0) -> None:
        self.timeout: float = timeout
        self._client: BleakClient | None = None

    async def scan(self) -> list[BLEDevice]:
        """Scans for nearby BLE devices and returns discovered devices."""

        return await BleakScanner.discover(timeout=self.timeout)

    async def connect(self, target: str | BLEDevice) -> None:
        """Connects to a BLE device given its MAC address, UUID, or BLEDevice instance."""

        self._client = BleakClient(target, timeout=self.timeout)
        try:
            await self._client.connect()
        except BleakError as e:
            print(f"Connection error: {e}")
            self._client = None

    async def disconnect(self) -> None:
        """Disconnects from the currently connected BLE device."""

        if self._client and self._client.is_connected:
            try:
                await self._client.disconnect()
            except BleakError as e:
                print(f"Disconnect error: {e}")
            finally:
                self._client = None

    @property
    def is_connected(self) -> bool:
        """Checks if there is an active connection."""

        return self._client is not None and self._client.is_connected


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
    print(f"\n[{target_device}] Connecting...")
    await bt.connect(target_device)

    if not bt.is_connected:
        print(f"[{target_device}] Failed to connect.")
        return

    print(f"[{target_device}] Connected successfully!")

    print(f"[{target_device}] Disconnecting in 2 seconds...")
    await asyncio.sleep(2)
    await bt.disconnect()

    print(f"[{target_device}] Disconnected.")


if __name__ == "__main__":
    asyncio.run(main())
