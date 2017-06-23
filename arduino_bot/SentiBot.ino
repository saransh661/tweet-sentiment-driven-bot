char command;
int konnected;
int motor_pin1 = 9;
int motor_pin2 = 10;
int k1, k2;

void drive(int k1 , int k2){
      digitalWrite(motor_pin1, k1);
      digitalWrite(motor_pin2, k2);
  }

void setup() {
  
  Serial.begin(9600);

}

void loop() {
  konnected = Serial.available();

  if(konnected) {
    command = Serial.read(); 
    
    if(command == 'F'){
        drive(1,0);  
    }

     else if (command == 'B'){
        drive(0,1);
     }

     else if (command == 'N'){
        drive(0,0);
     }
     
  }
}


