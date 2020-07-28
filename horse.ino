#include <Ultrasonic.h>
#include <Servo.h>

Ultrasonic ultrasonic(2, 3);
Servo servoLF, servoRF, servoLB, servoRB;
const int A = 70;
const int B = 80;
const int C = 100;
const int D = 110;
String LF = "90",RF = "90",LB = "90",RB = "90";
String MoveInfo;

void setup() {
  Serial.begin(9600);
  servoLF.attach(11); servoRF.attach(9);
  servoLB.attach(10); servoRB.attach(6);
  setLF(90);
  setRF(90);
  setLB(90);
  setRB(90);
}

void loop() {
  
  while(Serial.available())
  {
      String received = Serial.readStringUntil('\n');
      String function = getValue(received, ',', 0);
      
      if(function == "MoveLeg"){
        LF = getValue(received, ',', 1);
        RF = getValue(received, ',', 2);
        LB = getValue(received, ',', 3);
        RB = getValue(received, ',', 4);
        setLF(LF.toInt()); setRF(RF.toInt());
        setLB(LB.toInt()); setRB(RB.toInt());
      }else 
      if(function == "getDistance"){
        int distance = ultrasonic.read();
        Serial.println(distance);
      }else
      if(function == "getLegStatus"){
        String LegStatus = String(servoLF.read()) + "," + String(servoRF.read()) + "," + String(servoLB.read()) + "," + String(servoRB.read());
        Serial.println(LegStatus);
      }else
      if(function == "reset"){
        setLF(90); setRF(90);
        setLB(90); setRB(90);
      }else{
        Serial.println(received);
      }
  }
  
}

void setLF(float r) {
  servoLF.write(r+2);
}
void setRF(float r) {
  servoRF.write(180-r);
}
void setLB(float r) {
  servoLB.write(r+7);
}
void setRB(float r) {
  servoRB.write(180-r-7);
}
String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;
    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}
