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


void setup() {
  servo1.attach(servoPin1);
  servo2.attach(servoPin2);
  servo3.attach(servoPin3);


  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);

  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);


  servo1.write(0);
  Serial.begin(9600);
}

void loop() {
  long dur1, dis1, dur2, dis2;

  digitalWrite(trigPin1, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin1, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin1, LOW);

  digitalWrite(trigPin2, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin2, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin2, LOW);

  dur1 = pulseIn(echoPin1,HIGH);
  dis1 = (dur1 * 0.034 / 2);

  dur2 = pulseIn(echoPin2,HIGH);
  dis2 = (dur2 * 0.034 / 2);

  Serial.print("Distance 1: ");
  Serial.println(dis1);

  Serial.print("Distance 2: ");
  Serial.println(dis2);

    if (Serial.available() > 0) {
    int command = Serial.read();
    if (command == '1' || command == '2')
    {
      //đẩy:
      servo3.write(160);
      delay(150);
      servo3.write(0);
      
    //hữu cơ
    if (command == '1') 
    {
      if (dis1 <= 5)
      {
      servo1.write(160);
      delay(150);
      servo1.write(0);
    }
    }

    //vô cơ
    else if (command == '2')
    {
      if (dis2 <= 5)
      {
      servo2.write(160);
      delay(150);
      servo2.write(0);
    }
    }
  }

}
}