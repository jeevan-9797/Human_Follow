# 🤖 Human Following Robot

A Wi-Fi controlled human-following robot that uses a **phone camera, Python/OpenCV, and ESP32-S3** to detect a red marker attached to a person's leg and control the robot's movement.

The system detects the marker's position in the camera frame and sends movement commands to the ESP32-S3 over **Wi-Fi using UDP**.

---

## 🚀 Features

* 📱 Phone camera used as the vision system
* 👁️ Red-marker detection using OpenCV
* 🎯 Tracks a red marker attached to the user's leg
* ↔️ Determines whether the marker is LEFT, CENTER, or RIGHT
* 📡 Wi-Fi communication between laptop and ESP32-S3
* ⚡ UDP-based low-latency robot control
* 🚗 Forward, left, right, and stop movement
* 📏 Configurable following distance
* 🐢 Low-speed operation for safe testing

---

## 🧠 How It Works

```text
        Phone Camera
             │
             │ Wi-Fi
             ▼
      ┌───────────────┐
      │ Python +      │
      │ OpenCV        │
      │               │
      │ Red Marker    │
      │ Detection     │
      └───────┬───────┘
              │
              │ UDP Commands
              ▼
      ┌───────────────┐
      │   ESP32-S3    │
      │               │
      │ Motor Control │
      └───────┬───────┘
              │
              ▼
        Motor Driver
              │
              ▼
        Robot Motors
```

---

## 🛠️ Technologies Used

### Software

* Python
* OpenCV
* NumPy
* Arduino IDE
* ESP32 Arduino framework

### Hardware

* ESP32-S3
* Motor driver
* DC geared motors
* Robot chassis
* Smartphone camera
* Battery/power supply
* Red marker attached to the user's leg

---

## 📁 Project Structure

```text
Human_Following_Robot/
│
├── human_following.py
├── camera_test.py
├── marker_detection.py
├── ble_test.py
├── auto_control.py
│
├── esp32_robot_control/
│   └── esp32_robot_control.ino
│
├── images/
│   └── test images
│
└── README.md
```

---

## ⚙️ Setup

### 1. Install Python Dependencies

Create/activate your Python virtual environment and install:

```bash
pip install opencv-python numpy
```

---

### 2. Configure Phone Camera

The phone camera provides an MJPEG video stream.

Update the camera URL in:

```python
human_following.py
```

Example:

```python
CAMERA_URL = "http://PHONE_IP:8080/video"
```

Make sure the phone and laptop are connected to the same Wi-Fi network.

---

### 3. Configure ESP32

Set the Wi-Fi credentials in:

```cpp
esp32_robot_control.ino
```

```cpp
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";
```

The ESP32 listens for UDP commands on:

```text
Port: 4210
```

---

### 4. Upload ESP32 Code

Open the Arduino sketch in Arduino IDE.

Select:

```text
Board: ESP32S3 Dev Module
```

Select the correct COM port and upload the code.

After uploading, open Serial Monitor at:

```text
115200 baud
```

The ESP32 should display its IP address.

---

## 🎮 Robot Commands

The ESP32 receives movement commands through UDP.

| Command | Action  |
| ------- | ------- |
| `F`     | Forward |
| `L`     | Left    |
| `R`     | Right   |
| `S`     | Stop    |

Additional turning commands may be used depending on the current control implementation.

---

## 🎯 Marker Tracking

The robot uses a red marker as the tracking target.

The camera frame is divided into three major zones:

```text
┌─────────────────────────────────────────┐
│                                         │
│       LEFT       CENTER       RIGHT     │
│                                         │
│       0-160      160-480      480-640   │
│                                         │
└─────────────────────────────────────────┘
```

A large center region is used to prevent small marker movements from causing unnecessary steering corrections.

---

## 📏 Following Distance

The system can be calibrated using a known marker distance.

For the current configuration:

```text
Target distance: 5 inches
```

The marker is placed at the target distance and calibrated before autonomous following is started.

---

## 🐢 Speed

The current robot speed is configured for slow and controlled movement.

```text
Motor PWM: 69
```

This is intended for testing the human-following system safely.

---

## ▶️ Running the Project

### Start the ESP32

1. Power the robot.
2. ESP32 connects to Wi-Fi.
3. Check its IP address using Serial Monitor.
4. Confirm UDP port `4210` is active.

### Start the Python program

Run:

```bash
python human_following.py
```

The camera window should open.

Place the red marker in front of the camera and perform the required calibration.

The Python program then:

1. Captures the phone camera feed.
2. Detects the red marker.
3. Calculates its position.
4. Determines the required movement.
5. Sends a UDP command to the ESP32.
6. ESP32 controls the motors.

---

## 🔧 Troubleshooting

### Camera not connecting

Check:

* Phone and laptop are on the same Wi-Fi network.
* Phone camera streaming application is running.
* Camera IP address is correct.
* `/video` endpoint is correct.

### ESP32 not receiving commands

Check:

* Laptop and ESP32 are on the same network.
* ESP32 IP address is correct.
* UDP port is `4210`.
* Windows firewall is not blocking Python/network communication.

### Robot moves in the wrong direction

Check the motor polarity and motor-driver wiring.

If necessary, reverse the motor direction in the ESP32 motor-control functions.

### Robot is too sensitive

Adjust the LEFT/CENTER/RIGHT boundaries in the Python tracking code.

---

## 📌 Current Configuration

```text
Controller       : ESP32-S3
Vision            : Smartphone camera
Computer vision   : Python + OpenCV
Communication     : Wi-Fi UDP
UDP Port          : 4210
Target marker     : Red
Target distance   : 5 inches
Motor speed       : 69
Tracking zones    : Left / Center / Right
```

---

## 🔮 Future Improvements

* Human/person detection instead of a colored marker
* Better distance estimation
* Automatic obstacle detection
* Ultrasonic/ToF obstacle avoidance
* PID-based steering
* Automatic speed adjustment
* Improved camera streaming latency
* Autonomous path following
* Emergency stop system
* Battery monitoring

---

## 👥 Project

**Human Following Robot**

Developed as a robotics/computer-vision project combining:

**Python + OpenCV + Wi-Fi + ESP32-S3 + Motor Control**
