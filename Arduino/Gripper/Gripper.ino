#include <Arduino.h>
#include <ESP32Servo.h>

#define SERVO 26
#define SERVO_ROT 27
#define CLOSE 10
#define OPEN 170

Servo gripper;
Servo rotation;

void setup() {
  Serial.begin(9600);

  pinMode(SERVO, OUTPUT);
  pinMode(SERVO_ROT, OUTPUT);

  gripper.attach(SERVO, 500, 2500);
  rotation.attach(SERVO_ROT, 500, 2500);
}

void loop() {
  static char reading[20];
  static byte i = 0, val1 = CLOSE, val2 = 90;

  while (Serial.available() == 0) {
  }

  while (Serial.peek() != ' ' && Serial.peek() != '\n') {
    reading[i] = Serial.read();
    i++;
    delay(10);
  }
  reading[i] = '\0';

  val1 = atoi(reading);

  if (Serial.read() == ' ') {
    i = 0;
    while (Serial.peek() != ' ' && Serial.peek() != '\n') {
      reading[i] = Serial.read();
      i++;
      delay(10);
    }
    reading[i] = '\0';
    val2 = atoi(reading);
  }

  val1 = map(val1, 0, 100, OPEN, CLOSE);

  gripper.write(val1);
  rotation.write(val2);

  i = 0;

  while (Serial.available() != 0) {
    Serial.read();
  }
}
