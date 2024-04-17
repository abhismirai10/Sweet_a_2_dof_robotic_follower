//here communication is 120,90 just that yaw,pitch 

#include <Servo.h>

Servo yaw_servo;
Servo pitch_servo;

int yaw_angle = 90;
int pitch_angle = 90;

#define xy_servo 9
#define xz_servo 10

unsigned long previousMillis = 0; // will store last time servo was updated
const long interval = 30;        // interval at which to update servo (milliseconds)

void setup() {
  Serial.begin(9600);
  yaw_servo.attach(xy_servo);
  pitch_servo.attach(xz_servo);
}

void updateServo(Servo& servo, int& angle, int error) {
  if (abs(error) > 2) { // Only adjust if error is significant
    angle -= error / 30; // Example proportional control factor
    angle = constrain(angle, 60, 120); // Constrain angle to prevent over-rotation
    servo.write(angle);
  }
}

void loop() {
  unsigned long currentMillis = millis();

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read the command until newline
    int commaIndex = command.indexOf(',');
    
    if (commaIndex != -1) {
      int yaw_error = command.substring(0, commaIndex).toInt();
      int pitch_error = command.substring(commaIndex + 1).toInt();
      
      if(currentMillis - previousMillis >= interval) {
        previousMillis = currentMillis;   
        updateServo(yaw_servo, yaw_angle, yaw_error);
        updateServo(pitch_servo, pitch_angle, pitch_error);
      }
    }
  }
}



