import cv2
import numpy as np

# Load image
image = cv2.imread("IMG_20260809_094639.jpg.jpeg")

if image is None:
    print("Image not found!")
    exit()

# Resize image
image = cv2.resize(image, (800, 600))

# Convert to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Red color ranges
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])

lower_red2 = np.array([170, 100, 100])
upper_red2 = np.array([180, 255, 255])

# Create mask
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

mask = mask1 | mask2

# Find contours
contours, _ = cv2.findContours(
    mask,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

if contours:

    # Find largest contour
    largest = max(contours, key=cv2.contourArea)

    area = cv2.contourArea(largest)

    print("Largest contour area:", area)

    if area > 500:

        # Bounding box
        x, y, w, h = cv2.boundingRect(largest)

        # Center
        center_x = x + w // 2
        center_y = y + h // 2

        print("MARKER DETECTED")
        print("Center X:", center_x)
        print("Center Y:", center_y)

        # Draw rectangle
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

        # Display coordinates
        cv2.putText(
            image,
            f"({center_x}, {center_y})",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    else:
        print("Marker too small")

else:
    print("MARKER NOT FOUND")

# Show results
cv2.imshow("Marker Detection", image)
cv2.imshow("Mask", mask)

cv2.waitKey(0)
cv2.destroyAllWindows()