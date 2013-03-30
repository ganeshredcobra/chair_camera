int analogPin = 2;     
int sens;
void setup()
{
  Serial.begin(9600);          
}

void loop()
{
  sens = ReadSens_and_Condition();
  //Serial.println(val);
 if(sens>900) 
 {
   Serial.println(1);
 }
 else
 {
   Serial.println(0);
 }
  delay(100)  ;
  
}
int ReadSens_and_Condition(){
  int i;
  int sval = 0;

  for (i = 0; i < 5; i++){
    sval = sval + analogRead(analogPin);    // sensor on analog pin 0
  }

  sval = sval / 5;    // average
  //sval = sval / 4;    // scale to 8 bits (0 - 255)
  //sval = 255 - sval;  // invert output
  return sval;
}
