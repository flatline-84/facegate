#include <Braccio.h>
#include <Servo.h>
///#include <Serial.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

// Five arm components x 2 (name + rotation value), +1 for end char? Not sure.
char buffer[11];

void setup() {  
  //Initialization functions and set up the initial position for Braccio
  //All the servo motors will be positioned in the "safety" position:
  //Base (M1):90 degrees
  //Shoulder (M2): 45 degrees
  //Elbow (M3): 180 degrees
  //Wrist vertical (M4): 180 degrees
  //Wrist rotation (M5): 90 degrees
  //gripper (M6): 10 degrees
  Braccio.begin();
  Serial.begin(9600);
  //Wait for it to connect
  while (!Serial)
  {;}

  /*
  Step Delay: a milliseconds delay between the movement of each servo.  Allowed values from 10 to 30 msec.
  M1=base degrees. Allowed values from 0 to 180 degrees
  M2=shoulder degrees. Allowed values from 15 to 165 degrees
  M3=elbow degrees. Allowed values from 0 to 180 degrees
  M4=wrist vertical degrees. Allowed values from 0 to 180 degrees
  M5=wrist rotation degrees. Allowed values from 0 to 180 degrees
  M6=gripper degrees. Allowed values from 10 to 73 degrees. 10: the toungue is open, 73: the gripper is closed.
  */
  // the arm is aligned upwards  and the gripper is closed
                        //(step delay, M1, M2, M3, M4, M5, M6);
  Braccio.ServoMovement(20,         90, 90, 90, 90, 90,  73); 
}

void loop() {

  if(Serial.available() > 0)
  {
    // This is block so not great
    //Termination char is \r
    Serial.readBytesUntil('\r', buffer, 10);
  }

  //Should be getting base
  if (buffer[0] == 'b')
  {
    Braccio.ServoMovement(20, buffer[1], buffer[3], buffer[5], buffer[7], buffer[9], 73);
  }
  else 
  {
    for (int i = 0; i < 11; ++i)
    {
      buffer[i] = '\0';
    }
  }



  //-----------------------------\\
  //------------Test-------------\\
  //-----------------------------\\

  while(1)
  {
    Serial.println("READY");
    Serial.println(" ");
    while(Serial.available()<1);//if no input, just wait
//     if(Serial.read()=='0')
//     {
//          Serial.println("0 received");
//    Serial.println(" ");
//        Braccio.ServoMovement(20,         90, 90, 90, 90, 90,  0); 
//
//
//     }//end of if
     if(Serial.read()=='1')
     {
          Serial.println("1 Received");
    Serial.println(" ");
       Braccio.ServoMovement(20, 0, 45, 55, 45, 90,  10); //Bend to pick up
       delay(500);
       Braccio.ServoMovement(10, 0, 45, 55, 45, 90,  73); //Close Claw
       delay(500);
       Braccio.ServoMovement(20, 90, 90, 55, 90, 90,  73); 
       delay(500);
       Braccio.ServoMovement(20, 90, 45, 55, 45, 90,  73); 
       delay(500);
       Braccio.ServoMovement(20, 90, 45, 55, 45, 90,  10);

       delay(1000);
       Braccio.ServoMovement(20,         90, 90, 90, 90, 90,  73); 


     }//end of if




  }

}
