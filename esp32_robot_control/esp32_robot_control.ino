#include <WiFi.h>
#include <WiFiUdp.h>


// =====================================================
// WIFI
// =====================================================

const char* ssid = "K";
const char* password = "11223344";


// =====================================================
// UDP
// =====================================================

WiFiUDP udp;

const int udpPort = 4210;

char incomingPacket[50];


// =====================================================
// L298N MOTOR PINS
// =====================================================

#define ENA 1
#define IN1 2
#define IN2 3

#define IN3 14
#define IN4 41
#define ENB 42


// =====================================================
// MOTOR SPEED
// =====================================================

int baseSpeed = 69;


// =====================================================
// STOP
// =====================================================

void stopRobot()
{
    analogWrite(ENA, 0);
    analogWrite(ENB, 0);

    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);

    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
}


// =====================================================
// FORWARD
// =====================================================

void moveForward()
{
    analogWrite(ENA, 69);
    analogWrite(ENB, 69);

    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);

    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
}


// =====================================================
// GENTLE LEFT
// =====================================================

void gentleLeft()
{
    analogWrite(ENA, 45);
    analogWrite(ENB, 69);

    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);

    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
}


// =====================================================
// STRONG LEFT
// =====================================================

void strongLeft()
{
    analogWrite(ENA, 25);
    analogWrite(ENB, 69);

    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);

    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
}


// =====================================================
// GENTLE RIGHT
// =====================================================

void gentleRight()
{
    analogWrite(ENA, 69);
    analogWrite(ENB, 45);

    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);

    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
}


// =====================================================
// STRONG RIGHT
// =====================================================

void strongRight()
{
    analogWrite(ENA, 69);
    analogWrite(ENB, 25);

    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);

    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
}


// =====================================================
// COMMAND
// =====================================================

void executeCommand(String command)
{
    command.trim();

    Serial.print("Command: ");
    Serial.println(command);


    if (command == "F")
    {
        moveForward();
    }

    else if (command == "L")
    {
        gentleLeft();
    }

    else if (command == "LL")
    {
        strongLeft();
    }

    else if (command == "R")
    {
        gentleRight();
    }

    else if (command == "RR")
    {
        strongRight();
    }

    else if (command == "S")
    {
        stopRobot();
    }

    else
    {
        stopRobot();
    }
}


// =====================================================
// SETUP
// =====================================================

void setup()
{
    Serial.begin(115200);


    pinMode(ENA, OUTPUT);
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);

    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
    pinMode(ENB, OUTPUT);


    stopRobot();


    // =================================================
    // WIFI
    // =================================================

    WiFi.mode(WIFI_STA);

    WiFi.begin(
        ssid,
        password
    );


    Serial.println();

    Serial.print(
        "Connecting to Wi-Fi"
    );


    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);

        Serial.print(".");
    }


    Serial.println();

    Serial.println(
        "Wi-Fi connected!"
    );


    Serial.print(
        "ESP32 IP address: "
    );

    Serial.println(
        WiFi.localIP()
    );


    // =================================================
    // UDP
    // =================================================

    udp.begin(
        udpPort
    );


    Serial.print(
        "UDP listening on port: "
    );

    Serial.println(
        udpPort
    );


    Serial.println();
    Serial.println(
        "=============================="
    );
    Serial.println(
        " HUMAN FOLLOWING ROBOT"
    );
    Serial.println(
        " SPEED: 69"
    );
    Serial.println(
        " WI-FI UDP MODE"
    );
    Serial.println(
        "=============================="
    );
}


// =====================================================
// LOOP
// =====================================================

void loop()
{
    int packetSize = udp.parsePacket();

    if (packetSize > 0)
    {
        Serial.print("UDP PACKET RECEIVED - Size: ");
        Serial.println(packetSize);

        int len = udp.read(
            incomingPacket,
            sizeof(incomingPacket) - 1
        );

        if (len > 0)
        {
            incomingPacket[len] = '\0';
        }

        Serial.print("DATA RECEIVED: [");
        Serial.print(incomingPacket);
        Serial.println("]");

        String command = String(incomingPacket);
        command.trim();

        if (command == "F")
        {
            Serial.println("MOVING FORWARD");
            moveForward();
        }
        else if (command == "S")
        {
            Serial.println("STOP");
            stopRobot();
        }
        else if (command == "L")
        {
            Serial.println("LEFT");
            gentleLeft();
        }
        else if (command == "R")
        {
            Serial.println("RIGHT");
            gentleRight();
        }
        else
        {
            Serial.println("UNKNOWN COMMAND");
            stopRobot();
        }
    }

    delay(5);
}