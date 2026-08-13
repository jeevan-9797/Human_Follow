import asyncio
from bleak import BleakClient, BleakScanner

DEVICE_NAME = "Human_Following_Robot"

RX_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"


async def main():

    print("Searching for ESP32-S3...")

    device = await BleakScanner.find_device_by_name(
        DEVICE_NAME,
        timeout=10
    )

    if device is None:
        print("ESP32-S3 not found!")
        return

    print("Found:", device.name)
    print("Address:", device.address)

    print("Connecting...")

    async with BleakClient(device) as client:

        print("Connected!")
        print()

        while True:

            command = input(
                "Enter command (L/F/R/S or Q to quit): "
            ).upper()

            if command == "Q":
                break

            if command not in ["L", "F", "R", "S"]:
                print("Invalid command")
                continue

            await client.write_gatt_char(
                RX_UUID,
                command.encode()
            )

            print("Sent:", command)


asyncio.run(main())