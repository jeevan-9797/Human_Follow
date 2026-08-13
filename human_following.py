import cv2
import numpy as np
import socket
import time
import threading


# =========================================================
# PHONE CAMERA
# =========================================================

CAMERA_URL = "http://10.34.36.126:8080/video"


# =========================================================
# ESP32
# =========================================================

ESP32_IP = "10.110.1.117"
UDP_PORT = 4210


# =========================================================
# CAMERA
# =========================================================

WIDTH = 640
HEIGHT = 480


# =========================================================
# FOLLOWING DISTANCE
# =========================================================

TARGET_DISTANCE = 5.0

DISTANCE_TOLERANCE = 0.5


# =========================================================
# UDP
# =========================================================

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)


def send_command(command):

    try:

        sock.sendto(
            command.encode(),
            (ESP32_IP, UDP_PORT)
        )

    except Exception as e:

        print("UDP ERROR:", e)


# =========================================================
# CAMERA THREAD
# =========================================================

class Camera:

    def __init__(self):

        self.frame = None

        self.running = True

        self.lock = threading.Lock()

        self.cap = cv2.VideoCapture(
            CAMERA_URL
        )

        # Try to reduce camera buffering
        self.cap.set(
            cv2.CAP_PROP_BUFFERSIZE,
            1
        )

        if not self.cap.isOpened():

            print()
            print("ERROR: Could not open phone camera")
            print(
                CAMERA_URL
            )

            self.running = False

            return


        print("Phone camera connected!")


        self.thread = threading.Thread(
            target=self.update,
            daemon=True
        )

        self.thread.start()


    def update(self):

        while self.running:

            ret, frame = self.cap.read()


            if not ret:

                time.sleep(0.01)

                continue


            frame = cv2.resize(
                frame,
                (WIDTH, HEIGHT)
            )


            # Keep ONLY newest frame
            with self.lock:

                self.frame = frame


    def get_frame(self):

        with self.lock:

            if self.frame is None:

                return None

            return self.frame.copy()


    def stop(self):

        self.running = False

        self.cap.release()


# =========================================================
# MAIN
# =========================================================

def main():

    print()
    print("======================================")
    print(" HUMAN FOLLOWING ROBOT")
    print(" Wi-Fi UDP CONTROL")
    print(" SPEED: 69")
    print(" TARGET: 5 INCHES")
    print("======================================")
    print()


    # =====================================================
    # START CAMERA
    # =====================================================

    camera = Camera()


    if not camera.running:

        return


    print(
        "Waiting for camera frames..."
    )


    start = time.time()


    while camera.get_frame() is None:

        if time.time() - start > 10:

            print(
                "ERROR: No camera frames received."
            )

            camera.stop()

            return


        time.sleep(0.02)


    print(
        "Camera feed working!"
    )


    # =====================================================
    # INITIAL STOP
    # =====================================================

    send_command("S")


    print()
    print("--------------------------------------")
    print("5 INCH CALIBRATION")
    print("--------------------------------------")
    print()
    print(
        "Place the RED marker exactly 5 inches"
    )
    print(
        "from the phone camera."
    )
    print()
    print(
        "Press C to calibrate."
    )
    print(
        "Press Q to quit."
    )
    print()


    # =====================================================
    # VARIABLES
    # =====================================================

    calibrated_height = None

    last_marker_time = time.time()

    last_command = "S"

    last_send_time = 0

    SEND_INTERVAL = 0.08

    LOST_TIMEOUT = 0.40


    # =====================================================
    # LOOP
    # =====================================================

    while True:

        frame = camera.get_frame()


        if frame is None:

            continue


        # =================================================
        # HSV
        # =================================================

        hsv = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2HSV
        )


        # =================================================
        # RED MASK
        # =================================================

        lower_red1 = np.array(
            [0, 100, 100]
        )

        upper_red1 = np.array(
            [10, 255, 255]
        )


        lower_red2 = np.array(
            [170, 100, 100]
        )

        upper_red2 = np.array(
            [180, 255, 255]
        )


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


        # =================================================
        # CLEAN MASK
        # =================================================

        kernel = np.ones(
            (5, 5),
            np.uint8
        )


        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            kernel
        )


        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_CLOSE,
            kernel
        )


        # =================================================
        # FIND CONTOURS
        # =================================================

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )


        # =================================================
        # DEFAULT
        # =================================================

        command = "S"

        position = "MARKER LOST"

        distance = 0

        marker_found = False

        marker_height = 0

        center_x = 320


        # =================================================
        # FIND MARKER
        # =================================================

        if len(contours) > 0:

            largest = max(
                contours,
                key=cv2.contourArea
            )


            area = cv2.contourArea(
                largest
            )


            # Ignore tiny red objects/noise

            if area > 300:

                marker_found = True

                last_marker_time = time.time()


                x, y, w, h = cv2.boundingRect(
                    largest
                )


                center_x = x + (w // 2)

                center_y = y + (h // 2)

                marker_height = h


                # =================================================
                # DISTANCE
                # =================================================

                if calibrated_height is not None:

                    if marker_height > 0:

                        distance = (
                            TARGET_DISTANCE
                            *
                            calibrated_height
                            /
                            marker_height
                        )


                # =================================================
                # LARGE CENTER AXIS
                #
                # 640 pixel image
                #
                # 0       160             480       640
                # |--------|---------------|---------|
                #    LEFT       CENTER         RIGHT
                #
                # =================================================

                if center_x < 160:

                    position = "LEFT"

                elif center_x < 480:

                    position = "CENTER"

                else:

                    position = "RIGHT"


                # =================================================
                # MOVEMENT
                # =================================================

                if calibrated_height is None:

                    command = "S"


                else:

                    # =============================================
                    # MORE THAN 5.5 INCHES
                    # FOLLOW
                    # =============================================

                    if distance > 5.5:

                        if center_x < 160:

                            # Marker on LEFT
                            command = "RR"

                        elif center_x < 480:

                            # Marker CENTER
                            command = "F"

                        else:

                            # Marker RIGHT
                            command = "LL"


                    # =============================================
                    # 4.5 - 5.5 INCHES
                    # STOP
                    # =============================================

                    elif distance >= 4.5:

                        command = "S"


                    # =============================================
                    # LESS THAN 4.5 INCHES
                    # STOP
                    # =============================================

                    else:

                        command = "S"


                # =================================================
                # DRAW BOX
                # =================================================

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )


                # =================================================
                # DRAW CENTER
                # =================================================

                cv2.circle(
                    frame,
                    (center_x, center_y),
                    6,
                    (255, 0, 0),
                    -1
                )


                # =================================================
                # DRAW AXIS
                # =================================================

                cv2.line(
                    frame,
                    (160, 0),
                    (160, HEIGHT),
                    (255, 255, 255),
                    1
                )


                cv2.line(
                    frame,
                    (480, 0),
                    (480, HEIGHT),
                    (255, 255, 255),
                    1
                )


        # =================================================
        # MARKER LOST
        # =================================================

        if (
            time.time() - last_marker_time
            > LOST_TIMEOUT
        ):

            command = "S"

            position = "MARKER LOST"


        # =================================================
        # SEND COMMAND
        # =================================================

        now = time.time()


        if (
            command != last_command
            or
            now - last_send_time
            > SEND_INTERVAL
        ):

            send_command(
                command
            )

            last_command = command

            last_send_time = now


        # =================================================
        # TEXT
        # =================================================

        cv2.putText(
            frame,
            "POSITION: " + position,
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.70,
            (0, 255, 0),
            2
        )


        cv2.putText(
            frame,
            "COMMAND: " + command,
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.70,
            (0, 255, 255),
            2
        )


        if calibrated_height is None:

            cv2.putText(
                frame,
                "PLACE MARKER AT 5 INCHES - PRESS C",
                (20, 105),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 0, 255),
                2
            )

        else:

            cv2.putText(
                frame,
                f"TARGET: 5.0 in  CURRENT: {distance:.1f} in",
                (20, 105),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 0),
                2
            )


        # =================================================
        # SHOW CAMERA
        # =================================================

        cv2.imshow(
            "Human Following Robot",
            frame
        )


        # =================================================
        # SHOW MASK
        # =================================================

        cv2.imshow(
            "Marker Mask",
            mask
        )


        # =================================================
        # KEY
        # =================================================

        key = cv2.waitKey(1) & 0xFF


        # =================================================
        # CALIBRATION
        # =================================================

        if key == ord("c"):

            if marker_found:

                calibrated_height = marker_height


                print()
                print(
                    "================================"
                )

                print(
                    "5 INCH CALIBRATION COMPLETE"
                )

                print(
                    "Marker height:",
                    calibrated_height,
                    "pixels"
                )

                print(
                    "Target: 5 inches"
                )

                print(
                    "================================"
                )

                print()

            else:

                print(
                    "RED MARKER NOT DETECTED!"
                )


        # =================================================
        # QUIT
        # =================================================

        if key == ord("q"):

            print(
                "Stopping robot..."
            )

            send_command("S")

            break


    # =====================================================
    # CLEANUP
    # =====================================================

    send_command("S")

    camera.stop()

    sock.close()

    cv2.destroyAllWindows()


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    main()