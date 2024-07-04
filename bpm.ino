#include <PulseSensorPlayground.h>     //PulseSensorPlayground Library.   
const int PulseWire = 0;       // Sensor's purple wire connected to A0
int Threshold = 600;           // Determine heartbeat signal is true and which to ignore.
//decrease threshold will increase sensitivity
//increase threshold will decrease sensitivity                     
PulseSensorPlayground pulseSensor;  // Creates instance of PulseSensorPlayground object called "pulseSensor"

void setup() {   
  Serial.begin(115200);          // remember to set serial monitor to this as well
  
  analogReference(EXTERNAL); //read from AREF pin when it reads analog signls
  pulseSensor.analogInput(PulseWire);   
  pulseSensor.setThreshold(Threshold);   
  // used to see if started
   if (pulseSensor.begin()) {
    Serial.println(111111, DEC);  //Prints line for monitor
  } }
  
void loop() {
if (pulseSensor.sawStartOfBeat()) {            // Checks if heartbeat happened
int BPM = pulseSensor.getBeatsPerMinute();  //return as integer
 Serial.println(BPM, DEC);    // dec sends value as int rather than char and print value
}
  delay(30);                    // pauses for __ milliseconds
}

  
