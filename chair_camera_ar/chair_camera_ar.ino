// You can change the bounding values for the capacitive/touch
// sensor depending on what values work best for your setup
// + environmental factors
#define LOW_T       10    // lower bound for touch sensor
#define HIGH_T      60    // upper bound for touch sensor
#define LED         13    // LED output pin

// These are variables for the low-pass (smoothing) filter.
float prev_capI;    // previous capacitance interval
float filt_capI;    // filtered capacitance interval
float f_val = .07;  // 1 = no filter, 0.001 = max filter
unsigned int capLo; // duration when sensor reads LOW
unsigned int capHi5; // duration when sensor reads HIGH

void setup()
{
  Serial.begin(9600);

  pinMode(LED, OUTPUT);
  pinMode(4, OUTPUT);    // output pin
  pinMode(5, INPUT);     // input pin
 
}

void loop()
{  
  // clear out the capacitance time interval measures at start
  // of each loop iteration
  capHi5 = 0;
  
  capLo = 0;

  // average over 4 times to remove jitter
  for (int i=0; i < 4 ; i++ )
  {      
    // LOW-to-HIGH transition
    digitalWrite(4, HIGH);   

    // measure duration while the sense pin is not high
    while (digitalRead(5) != 1)
      capLo++;
    delay(1);

    //  HIGH-to-LOW transition
    digitalWrite(4, LOW);             

    // measure duration while the sense pin is high
    while(digitalRead(5) != 0 )    
     capHi5++; 
    delay(1);
    
  }

 

   // Smoothed Low to High
if(capHi5 > 10)
  Serial.println(0);
else 
  Serial.println(1);
}
