import cv2
import numpy as np

# ==============================
# 1. LOAD IMAGE
# ==============================

image = cv2.imread("IMG_20260809_094639.jpg.jpeg")

if image is None:
    print("Image not found!")
    exit()


# ==============================
# 2. RESIZE IMAGE
# ==============================

image = cv2.resize(image, (800, 600))


# ==============================
# 3. CONVERT TO HSV
# ==============================

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


# ==============================
# 4. RED COLOR DETECTION
# ==============================

lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])

lower_red2 = np.array([170, 100, 100])
upper_red2 = np.array([180, 255, 255])


# Create masks
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

mask = mask1 | mask2


# ==============================
# 5. FIND CONTOURS
# ==============================

contours, _ = cv2.findContours(
    mask,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)


# ==============================
# 6. DETECT MARKER
# ==============================

if contours:

    # Find largest detected object
    largest = max(contours, key=cv2.contourArea)

    area = cv2.contourArea(largest)

    print("Largest contour area:", area)

    if area > 500:

        # Get bounding box
        x, y, w, h = cv2.boundingRect(largest)

        # Find center
        center_x = x + w // 2
        center_y = y + h // 2

        print("MARKER DETECTED")
        print("Center X:", center_x)
        print("Center Y:", center_y)


        # ==============================
        # 7. LOCATE MARKER
        # ==============================

        if center_x < 266:

            position = "LEFT"

        elif center_x < 534:

            position = "CENTER"

        else:

            position = "RIGHT"


        print("Position:", position)


        # ==============================
        # 8. DECIDE ROBOT MOVEMENT
        # ==============================

        if position == "LEFT":

            command = "LEFT"

        elif position == "CENTER":

            command = "FORWARD"

        elif position == "RIGHT":

            command = "RIGHT"

        else:

            command = "STOP"


        print("Robot Command:", command)


        # ==============================
        # 9. DRAW MARKER
        # ==============================

        cv2.rectangle(
            image,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            3
        )


        # Draw center point
        cv2.circle(
            image,
            (center_x, center_y),
            7,
            (255, 0, 0),
            -1
        )


        # ==============================
        # 10. DISPLAY POSITION
        # ==============================

        cv2.putText(
            image,
            position,
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 255, 0),
            3
        )


        # Display command
        cv2.putText(
            image,
            "Command: " + command,
            (30, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            3
        )

    else:

        print("Marker too small")
        print("Robot Command: STOP")


else:

    print("MARKER NOT FOUND")
    print("Robot Command: STOP")


# ==============================
# 11. SHOW RESULTS
# ==============================

cv2.imshow("Marker Detection", image)

cv2.imshow("Mask", mask)


# Wait for key
cv2.waitKey(0)

# Close windows
cv2.destroyAllWindows()