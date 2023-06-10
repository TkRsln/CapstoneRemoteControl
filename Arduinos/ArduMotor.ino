


/*
//Coded by Utku ARSLAN
//
//10.06.2023
//Apache-2.0 license

//This code is responsible from rotating motors with L298 with received data from Raspberry PI via Usb/Serial Protocol
*/

String temp="";
int left_motor=1500;
int right_motor=1500;

int dir1PinA = 2;
int dir2PinA = 3;
int speedPinA = 9; // PWM pini, hız kontrolü için
 
// Motor 2
 
int dir1PinB = 4;
int dir2PinB = 5;
int speedPinB = 10; // PWM pini, hız kontrolü için
//d3(1) - EN1/ D5(9)-EN2 / D9(13)-EN3 / D10(14)-EN4


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  pinMode(dir1PinA,OUTPUT);
  pinMode(dir2PinA,OUTPUT);
  pinMode(speedPinA,OUTPUT);
  pinMode(dir1PinB,OUTPUT);
  pinMode(dir2PinB,OUTPUT);
  pinMode(speedPinB,OUTPUT);

  
}

void update_motors(){
  if(left_motor==1500){
    
    analogWrite(speedPinA, 0);

    //digitalWrite(l1,LOW);
    //digitalWrite(l2,LOW);
  }else{
    if(left_motor>1500){
      int v = (int)( (1-( (1900-left_motor) /400.0)) *255);
      digitalWrite(dir1PinA, LOW);
      digitalWrite(dir2PinA, HIGH);
      analogWrite(speedPinA, v);
    }else{
      int v=(int)((1-((left_motor-1100)/400.0))*255);
      digitalWrite(dir1PinA, HIGH);
      digitalWrite(dir2PinA, LOW);   
      analogWrite(speedPinA, v);
    }
  }

  if(right_motor==1500){
    
    analogWrite(speedPinB, 0);
    //digitalWrite(r1,LOW);
    //digitalWrite(r2,LOW);
  }else{
    if(right_motor>1500){
      int v = (int)( (1-( (1900-left_motor) /400.0)) *255);
      digitalWrite(dir1PinB, LOW);
      digitalWrite(dir2PinB, HIGH);
      analogWrite(speedPinB, v);
      //digitalWrite(r1,LOW);
      //analogWrite(r2,(int)((1900-right_motor)/400.0*255));
    }else{
      int v=(int)((1-((left_motor-1100)/400.0))*255);
      digitalWrite(dir1PinB, HIGH);
      digitalWrite(dir2PinB, LOW); 
      analogWrite(speedPinB, v);
      //digitalWrite(r2,LOW);
      //analogWrite(r1,(int)((1900-right_motor)/400.0*255));   
    }
  }
  
}
void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0){
      char c =Serial.read();
      if(c==':'){
        left_motor=temp.toInt();
        temp="";
        update_motors();
      }else if(c==';'){
        right_motor=temp.toInt();
        temp="";
        update_motors();
      }else{
        temp+=c;
      }
  }
}
