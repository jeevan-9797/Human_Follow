import cv2
import numpy as np
import asyncio

from bleak import BleakClient, BleakScanner


# ==========================================
# BLE SETTINGS
# ==========================================

DEVICE_NAME = "Human_Following_Robot"

RX_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"


# ==========================================
# IMAGE SETTINGS
# ==========================================

IMAGE_FILE = "IMG_20260809_094639.jpg.jpeg"


# ==========================================
# SEND COMMAND THROUGH BLE
# ==========================================

async def send_command(command):

    print("Searching for ESP32-S3...")

    device = await BleakScanner.find_device_by_name(
        DEVICE_NAME,
        timeout=10
    )

    if device is None:

        print("ESP32-S3 not found!")

        return

    print("ESP32 found")

    async with BleakClient(device) as client:

        print("BLE Connected")

        await client.write_gatt_char(
            RX_UUID,
            command.encode()
        )

        print("Sent:", command)


# ==========================================
# LOAD IMAGE
# ==========================================

image = cv2.imread(IMAGE_FILE)

if image is None:

    print("Image not found!")

    exit()


# ==========================================
# RESIZE
# ==========================================

image = cv2.resize(image, (800, 600))


# ==========================================
# HSV
# ==========================================

hsv = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2HSV
)


# ==========================================
# RED DETECTION
# ==========================================

lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])

lower_red2 = np.array([170, 100, 100])
upper_red2 = np.array([180, 255, 255])


mask1 = cv2.inRange(
    hsv,
    lower_red1,
    upper_red1
)

mask2 = cv2.inRange(
    hsv,
    lower_red2,
    upper_red2
)

mask = mask1 | mask2


# ==========================================
# FIND CONTOURS
# ==========================================

contours, _ = cv2.findContours(
    mask,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)


# ==========================================
# DETECTION
# ==========================================

if contours:

    largest = max(
        contours,
        key=cv2.contourArea
    )

    area = cv2.contourArea(largest)

    print("Area:", area)


    if area > 500:

        x, y, w, h = cv2.boundingRect(
            largest
        )


        # Marker center
        center_x = x + w // 2
        center_y = y + h // 2


        print("Marker detected")
        print("Center X:", center_x)
        print("Center Y:", center_y)


        # ==================================
        # POSITION
        # ==================================

        if center_x < 266:

            position = "LEFT"
            command = "L"


        elif center_x < 534:

            position = "CENTER"
            command = "F"


        else:

            position = "RIGHT"
            command = "R"


        print("Position:", position)
        print("Robot Command:", command)


        # ==================================
        # DRAW
        # ==================================

        cv2.rectangle(
            image,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            3
        )


        cv2.circle(
            image,
            (center_x, center_y),
            7,
            (255, 0, 0),
            -1
        )


        cv2.putText(
            image,
            position,
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 255, 0),
            3
        )


        cv2.putText(
            image,
            "Command: " + command,
            (30, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            3
        )


        # ==================================
        # SEND TO ESP32
        # ==================================

        asyncio.run(
            send_command(command)
        )


    else:

        print("Marker too small")

        asyncio.run(
            send_command("S")
        )


else:

    print("MARKER NOT FOUND")

    # Stop robot if marker disappears
    asyncio.run(
        send_command("S")
    )


# ==========================================
# DISPLAY
# ==========================================

cv2.imshow(
    "Human Following Robot",
    image
)

cv2.waitKey(0)

cv2.destroyAllWindows()