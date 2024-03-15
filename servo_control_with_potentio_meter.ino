// two dof robotics follower, just servo check using potentio meter
#include <Servo.h>

Servo yaw_servo;
Servo pitch_servo;

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
  int xy_pos = 10.0 + (160./1023.)*analogRead(pote_xy);
  int xz_pos = 10.0 + (160./1023.)*analogRead(pote_xz);
  Serial.print("the yaw angle: ");
  Serial.print(xy_pos);
  Serial.println(" the pitch angle: ");
  Serial.println(xz_pos);

  yaw_servo.write(xy_pos);
  pitch_servo.write(xz_pos);
}
