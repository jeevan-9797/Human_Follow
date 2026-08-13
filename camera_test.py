import cv2

# Phone camera stream
URL = "http://10.30.125.48:8080/video"

# Open phone camera
cap = cv2.VideoCapture(URL)

if not cap.isOpened():
    print("Could not connect to phone camera!")
    print("Check that the phone and laptop are on the same Wi-Fi.")
    exit()

print("Phone camera connected!")

while True:

    ret, frame = cap.read()

    if not ret:
        print("Could not receive frame")
        break

    # Resize for easier processing
    frame = cv2.resize(frame, (800, 600))

    cv2.imshow("Phone Camera", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()