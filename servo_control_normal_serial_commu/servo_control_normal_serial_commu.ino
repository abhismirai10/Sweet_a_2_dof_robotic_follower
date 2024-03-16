// servo control using a serial communication
#include <Servo.h>

Servo yaw_servo;
Servo pitch_servo;

//xy_servo is yaw and xz_servo is pitch 
//same for potentiometer
#define xy_servo 9
#define xz_servo 10

void setup() {
  Serial.begin(9600);
  yaw_servo.attach(xy_servo);
  pitch_servo.attach(xz_servo);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read the full command

    int yPos = command.indexOf('Y');
    int pPos = command.indexOf('P');

    if (yPos != -1 && pPos != -1) {
      // Extract yaw position, knowing 'P' follows 'Y'
      int yawPosition = command.substring(yPos + 1, pPos).toInt();

      // Extract pitch position, from 'P' to the end
      int pitchPosition = command.substring(pPos + 1).toInt();

      // Set servo positions if within valid range
      if (yawPosition >= 10 && yawPosition <= 170) 
      {
        yaw_servo.write(yawPosition);
      }
      if (pitchPosition >= 10 && pitchPosition <= 170) 
      {
        pitch_servo.write(pitchPosition);
      }

      delay(500);
    }
  }
}