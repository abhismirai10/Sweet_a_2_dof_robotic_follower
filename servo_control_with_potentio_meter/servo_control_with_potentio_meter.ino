// servo control using a potentiometer
#include <Servo.h>

Servo yaw_servo;
Servo pitch_servo;

//xy_servo is yaw and xz_servo is pitch 
//same for potentiometer
#define pote_xy A0
#define pote_xz A1
#define xy_servo 9
#define xz_servo 10

void setup() {
  Serial.begin(9600);
  pinMode(pote_xy, INPUT);
  pinMode(pote_xz, INPUT);
  yaw_servo.attach(xy_servo);
  pitch_servo.attach(xz_servo);
}

void loop() {
  //potentiometer output is in the range of 0 to 1023
  // so convering that to [10, 170]  
  int xy_pos = 50.0 + (90./1023.)*analogRead(pote_xy); //do not need whole 0 to 180 angle
  int xz_pos = 50.0 + (90./1023.)*analogRead(pote_xz);
  Serial.print("the yaw angle: ");
  Serial.print(xy_pos);
  Serial.println(" the pitch angle: ");
  Serial.println(xz_pos);

  yaw_servo.write(xy_pos);
  pitch_servo.write(xz_pos);
}
