#include <Braccio.h>
#include <Servo.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

#define BUF_SIZE 15

//extern int step_base = 0;
//extern int step_shoulder = 45;
//extern int step_elbow = 180;
//extern int step_wrist_rot = 180;
//extern int step_wrist_ver = 90;
//extern int step_gripper = 10;


uint8_t buffer[BUF_SIZE];

void serial_flush_buffer()
{
    while (Serial.read() >= 0)
    ; // do nothing
}

// Sequence 1 - Pick up/put down
void pickUp()
{
    Serial.println("Picking up object");
    Braccio.ServoMovement(20, 0, 90, 55, 90, 90, 10);
    delay(500);
    Braccio.ServoMovement(20, 0, 45, 55, 45, 90, 10); // Bend
    delay(500);
    Braccio.ServoMovement(10, 0, 45, 55, 45, 90, 65); // Close
    delay(300);
    Braccio.ServoMovement(20, 180, 90, 55, 90, 90, 65);
    delay(300);
    Braccio.ServoMovement(20, 180, 60, 55, 45, 90, 10);
    delay(300);
    Braccio.ServoMovement(20, 180, 85, 55, 45, 90, 10);
    delay(300);
    Braccio.ServoMovement(20, 1800, 90, 90, 90, 90, 65);
    delay(1000);

}


// Sequence 2 - Door Handle
void doorHandle()
{
    Serial.println("Opening door handle");
    Braccio.ServoMovement(20, 90, 45, 75, 75, 0, 10); // Bend
    delay(500);
    Braccio.ServoMovement(10, 90, 45, 75, 75, 0, 10); // Claw open
    delay(500);
    Braccio.ServoMovement(20, 90, 45, 75, 75, 0, 65); // Close Claw
    delay(500);
    Braccio.ServoMovement(20, 90, 45, 75, 75, 180, 65); // Rotate Claw
    delay(500);
    Braccio.ServoMovement(20, 90, 45, 75, 75, 180, 10); // Open Claw

    delay(1000);
    Braccio.ServoMovement(20, 90, 90, 90, 90, 90, 65); // Reset
}


// Sequence 3 - Wave
void wave()
{
    Serial.println("Waving!");
    Braccio.ServoMovement(20, 90, 90, 90, 90, 90, 65); // Bend 
    delay(500);
    Braccio.ServoMovement(10, 0, 45, 90, 90, 90, 10); // Claw open
    delay(500);
    Braccio.ServoMovement(20, 90, 90, 90, 90, 90, 10); //  Up claw open
    delay(500);
    Braccio.ServoMovement(20, 0, 60, 80, 80, 90, 10); // To the side
    delay(100);
    Braccio.ServoMovement(20, 0, 120, 100, 100, 90, 10); // Other side
    delay(100);
    Braccio.ServoMovement(20, 0, 60, 80, 80, 90, 10); // To the side
    delay(100);
    Braccio.ServoMovement(20, 0, 120, 100, 100, 90, 10); // Other side
    delay(100);
    Braccio.ServoMovement(20, 0, 45, 55, 45, 180, 10); //

    delay(1000);
    Braccio.ServoMovement(20, 90, 90, 90, 90, 90, 65); // Reset
}

void breathe()
{
}

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
    Braccio.ServoMovement(20,         90, 55, 75, 45, 90,  60); 
    Serial.begin(115200);
    //Wait for it to connect
    while (!Serial)
    {;}
    Serial.println("Connected!");

    /*
    Step Delay: a milliseconds delay between the movement of each servo.  Allowed values from 10 to 30 msec.
    M1=base degrees. Allowed values from 0 to 180 degrees
    M2=shoulder degrees. Allowed values from 15 to 165 degrees
    M3=elbow degrees. Allowed values from 0 to 180 degrees
    M4=wrist vertical degrees. Allowed values from 0 to 180 degrees
    M5=wrist rotation degrees. Allowed values from 0 to 180 degrees
    M6=gripper degrees. Allowed values from 10 to 65 degrees. 10: the toungue is open, 65: the gripper is closed.
    */
    // the arm is aligned upwards  and the gripper is closed
                        //(step delay, M1, M2, M3, M4, M5, M6);
//    
}

void loop() {

    if(Serial.available() > 0)
    {
        // This is block so not great
        //Termination char is \r
        Serial.readBytesUntil('\r', buffer, BUF_SIZE);
        Serial.println("Got some packets!");

        for (int i = 0; i < BUF_SIZE; ++i)
        {
          Serial.print(buffer[i]);
          Serial.print(", ");  
        }
        Serial.println();
        
    }

    

    //Should be getting b for beautifully move the robot arm
    if ((buffer[14] != '\0') && (buffer[13] != '\0') && (buffer[12] != '\0'))
    {
          for (int i = 0; i < BUF_SIZE; ++i)
          {
              buffer[i] = '\0';
          }
    }
    else if (buffer[0] == 'b')
    {
        Serial.println("Performing fine movement");
        Braccio.ServoMovement(10, buffer[1], buffer[3], buffer[5], buffer[7], buffer[9], buffer[11]);
    }
    // masterfully perform actions
    else if (buffer[0] == 'm')
    {
        
        switch(buffer[1])
        {
            case '1':
                pickUp();
                break;
            case '2':
                doorHandle();
                break;
            case '3':
                wave();
                break;
            default:
                breathe();
        }
//        serial_flush_buffer();
        Serial.println("masterful");
    }

    for (int i = 0; i < BUF_SIZE; ++i)
    {
        buffer[i] = '\0';
    }
}
