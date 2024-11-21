#include <Servo.h>
Servo myservo1;  
Servo myservo2;  
void setup() {
  //Gắn servo 1 vào chân 9, servo 2 vào chân 10 và servo 3 vào chân 11
  myservo1.attach(9);
  myservo2.attach(10); 
  Serial.begin(9600);
}

void loop() {
  //Python
  if (Serial.available() > 0) {
    int command = Serial.read();
    //hữu cơ
    if (command == '1') {
      myservo1.write(160); 
      delay(150);
      myservo1.write(0);    
    }
    //vô cơ
    else if (command == '2'){
      myservo2.write(160);
      delay(150);
      myservo2.write(0);
    }

    }
  }