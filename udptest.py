import socket
import time

ESP32_IP = "10.110.1.117"
UDP_PORT = 4210

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

print("Sending F commands...")

for i in range(10):
    print("Sending F", i + 1)

    sock.sendto(
        b"F",
        (ESP32_IP, UDP_PORT)
    )

    time.sleep(0.5)

print("Sending STOP")

sock.sendto(
    b"S",
    (ESP32_IP, UDP_PORT)
)

sock.close()

print("DONE")