
/*
//Coded by Utku ARSLAN
//
//10.06.2023
//Apache-2.0 license

//This code is responsible from transmitting the Sensor data to Raspberry PI vai Usb/Serial Protocol
*/


// Define the ultrasonic sensor pins
const int TRIGGER_PIN_1 = 2;
const int ECHO_PIN_1 = 3;
const int TRIGGER_PIN_2 = 2;
const int ECHO_PIN_2 = 3;
const int TRIGGER_PIN_3 = 2;
const int ECHO_PIN_3 = 3;

// Define variables for calculating distance
long duration;
//int distance_1=0,distance_2=0,distance_3=0;

void setup() {
  Serial.begin(9600); // Initialize serial communication
  setup_sensor();
}


void setup_sensor(){
  pinMode(TRIGGER_PIN_1, OUTPUT); // Set trigger pin as output
  pinMode(ECHO_PIN_1, INPUT); // Set echo pin as input
  pinMode(TRIGGER_PIN_2, OUTPUT); // Set trigger pin as output
  pinMode(ECHO_PIN_2, INPUT); // Set echo pin as input
  pinMode(TRIGGER_PIN_3, OUTPUT); // Set trigger pin as output
  pinMode(ECHO_PIN_3, INPUT); // Set echo pin as input
}
int measureDistance(int s_id){

  int tp=0;
  int ep=0;
  switch(s_id){
    case 0://Front
      tp=TRIGGER_PIN_1;
      ep=ECHO_PIN_1;
      break;
    case 1://Left
      tp=TRIGGER_PIN_2;
      ep=ECHO_PIN_2;
      break;
    case 2://Right
      tp=TRIGGER_PIN_3;
      ep=ECHO_PIN_3;
      break;
  }
  
  // Send a short pulse to the trigger pin
  digitalWrite(tp, LOW);
  delayMicroseconds(2);
  digitalWrite(tp, HIGH);
  delayMicroseconds(10);
  digitalWrite(tp, LOW);

  // Measure the duration of the pulse on the echo pin
  duration = pulseIn(ep, HIGH);

  delayMicroseconds(10);
  // Calculate the distance in centimeters
  int distance = int(duration * 0.034 / 2);
  return distance;
  /*
  switch(s_id){
    case 0://Front
      distance_1=distance;
      break;
    case 1://Left
      distance_2=distance;
      break;
    case 2://Right
      distance_3=distance;
      break;
  }

  // Print the distance to the serial monitor
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");*/

}

void loop() {
  //String s = String(measureDistance(0))+":"+String(measureDistance(1))+";"+String(measureDistance(2))+"/";
  String s = String(10)+":"+String(10)+";"+String(10)+"/";
  Serial.println(s);
  delay(100);
}
