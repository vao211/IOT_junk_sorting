#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
const int servoPin1 = 6;
const int servoPin2 = 7;
const int servoPin3 = 8;

const int trigPin1 = 9;
const int echoPin1 = 10;

const int trigPin2 = 11;
const int echoPin2 = 12;

long dur1, dis1, dur2, dis2;
int command = 0;

void setup() {
  servo1.attach(servoPin1);
  servo2.attach(servoPin2);
  servo3.attach(servoPin3);

  servo1.write(0);
  servo2.write(0);
  servo3.write(0);
  delay(200);

  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);

  Serial.begin(9600);
}
void getCommand(){
  if (Serial.available() > 0) {
  command = Serial.read() - '0';
  }
}
void Servo3(){
    getCommand();
  if (command == 1 || command ==2){
    servo3.write(70);
    delay(150);
    return;
  }
    servo3.write(0);
    delay(200);
    return;
}
void Servo1(){
  if (dis1 < 5 && dis1 > 0 && command ==1){
    servo1.write(130);
    command = 0;
    delay(150);
    return;
  }
    servo1.write(0);
    // delay(200);
}

void Servo2(){
  if (dis2 < 5 && dis2 >0 && command == 2){
    servo2.write(130);
    command = 0;
    delay(150);
    return;
  }
  servo2.write(0);
  // delay(200);
}
void loop() {
  Servo3();
  // Đo khoảng cách cảm biến 1
  digitalWrite(trigPin1, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin1, HIGH);
  delayMicroseconds(10);
  dur1 = pulseIn(echoPin1, HIGH);
  dis1 = (dur1 * 0.034 / 2);
  Servo1();

  Serial.print("Distance 1: ");
  Serial.println(dis1);

  // Đo khoảng cách cảm biến 2
  digitalWrite(trigPin2, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin2, HIGH);
  delayMicroseconds(10);
  dur2 = pulseIn(echoPin2, HIGH);
  dis2 = (dur2 * 0.034 / 2);
  Servo2();

  Serial.print("Distance 2: ");
  Serial.println(dis2);
}