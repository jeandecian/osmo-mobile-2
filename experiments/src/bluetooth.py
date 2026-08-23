import asyncio
from typing import Any

from bleak import BleakClient, BleakScanner
from bleak.backends.device import BLEDevice
from bleak.exc import BleakError


class Bluetooth:
    """Handles low-level BLE scanning, GATT connections, and communication."""

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

    def discover_services(self) -> list[dict[str, Any]]:
        """Returns all available GATT services and their characteristics."""

        if not self._client or not self.is_connected:
            return []

        services_data: list[dict[str, Any]] = []
        for service in self._client.services:
            char_list: list[dict[str, Any]] = []

            for char in service.characteristics:
                char_list.append(
                    {
                        "uuid": char.uuid,
                        "properties": list(char.properties),
                    }
                )

            services_data.append(
                {
                    "uuid": service.uuid,
                    "description": service.description,
                    "characteristics": char_list,
                }
            )

        return services_data

    def get_uuid_channels(self) -> dict[str, str | None]:
        """Extracts TX, RX, and Battery UUIDs directly from discovered services."""

        tx_uuid: str | None = None
        rx_uuid: str | None = None
        battery_uuid: str | None = None

        # Bluetooth Base UUID: 0000XXXX-0000-1000-8000-00805F9B34FB
        BLUETOOTH_SIG_SERVICE_PREFIX: str = "000018"  # 18XX
        BATTERY_LEVEL_ASSIGNED_CODE: str = "2a19"

        for service in self.discover_services():
            service_uuid: str = service["uuid"].lower()
            IS_BLUETOOTH_SERVICE: bool = service_uuid.startswith(
                BLUETOOTH_SIG_SERVICE_PREFIX
            )

            for char in service["characteristics"]:
                props: list[str] = char["properties"]
                uuid: str = char["uuid"]

                if (
                    "write-without-response" in props
                    and tx_uuid is None
                    and not IS_BLUETOOTH_SERVICE
                ):
                    tx_uuid = uuid

                if "notify" in props and rx_uuid is None and not IS_BLUETOOTH_SERVICE:
                    rx_uuid = uuid

                if BATTERY_LEVEL_ASSIGNED_CODE in uuid.lower() and battery_uuid is None:
                    battery_uuid = uuid

        return {"tx": tx_uuid, "rx": rx_uuid, "battery": battery_uuid}

    async def read_characteristic(self, char_uuid: str) -> bytes | None:
        """Reads raw byte payload from a specific characteristic."""

        if not self._client or not self.is_connected:
            return None

        try:
            return bytes(await self._client.read_gatt_char(char_uuid))
        except BleakError as e:
            print(f"Read error on {char_uuid}: {e}")
            return None


def find_target_device(devices: list[BLEDevice]) -> BLEDevice | None:
    """Finds a target device from a list of BLE devices."""

    for device in devices:
        device_name: str = (device.name or "").lower()

        if "dji" in device_name or "osmo" in device_name:
            return device

    return None


def print_gatt_services(services: list[dict[str, Any]]) -> None:
    if not services:
        print("Cannot discover services: Not connected.")
        return

    print("-" * 64)

    for service in services:
        print(f"[Service] {service['uuid']} ({service['description']})")

        for char in service["characteristics"]:
            props = ", ".join(char["properties"])
            print(f"  └── [Char] {char['uuid']} | Properties: [{props}]")

    print("-" * 64)


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

    print(f"[{target_device}] Discovering services...")

    services: list[dict[str, Any]] = bt.discover_services()
    print_gatt_services(services)

    channels: dict[str, str | None] = bt.get_uuid_channels()
    print(f"[{target_device}] UUID channels: {channels}")

    if channels["battery"]:
        raw_batt: bytes | None = await bt.read_characteristic(channels["battery"])
        if raw_batt:
            print(f"[{target_device}] Battery Level: {raw_batt[0]}%")

    print(f"[{target_device}] Disconnecting in 2 seconds...")
    await asyncio.sleep(2)
    await bt.disconnect()

    print(f"[{target_device}] Disconnected.")


if __name__ == "__main__":
    asyncio.run(main())
