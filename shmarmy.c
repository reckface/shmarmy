/******************************************************************************
Jim Lindblom @ SparkFun Electronics
April 28, 2016

Create a voltage divider circuit combining a flex sensor with a 47k resistor.
- The resistor should connect from A0 to GND.
- The flex sensor should connect from A0 to 3.3V
As the resistance of the flex sensor increases (meaning it's being bent), the
voltage at A0 should decrease.


******************************************************************************/
const int FLEX_PIN = A0; // Pin connected to voltage divider output

// Measure the voltage at 5V and the actual resistance of your
// 47k resistor, and enter them below:
const float VCC = 4.75; // Measured voltage of Ardunio 5V line
const float R_DIV = 10000.0; // Measured resistance of 3.3k resistor
const int ledPin = 13;

// Upload the code, then try to adjust these values to more
// accurately calculate bend degree.
const float STRAIGHT_RESISTANCE = 11550.0; // resistance when straight
const float BEND_RESISTANCE = 8130.0; // resistance at 90 deg

unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 50;    // the debounce time; increase if the output flickers

const int buzzer = 9;
int bCounter = 0;
int rCounter = 0;
boolean isPlaying = false;
boolean isPaused = true;
boolean isMax = false;
float oldAngle = 0;
static float Angle = 0;
int pulse = 1000;
int duration = 200;

long rInterval = 100;
long rMilli = 0;
long bInterval = 50;
long pInterval = 150;
long bMilli = 0;
long pMilli = 0;


void setup() 
{
  pinMode(FLEX_PIN, INPUT);
  pinMode(buzzer, OUTPUT);
  analogWrite(buzzer, 255);
  delay(500);
  analogWrite(buzzer, 0);
  pulsate();
  Serial.begin(9600);
}

void pulsate(){
  isPaused = false;
  for(int i = 0; i < 3; i++){      
    tone(buzzer, 1000, 200);
    delay(100);
    noTone(buzzer);
    delay(200);
  }
  isPaused = true;
}

void beep()
{
  if(isPaused)
    return;
  isPlaying = true;
  tone(buzzer, 1000, 20);
  //noTone(buzzer);
}

void pause(){
  noTone(buzzer);
  //analogWrite(buzzer, 0);
  isPlaying = false;
}

void loop()
{
  
  unsigned long currentMillis = millis();
  
  if(currentMillis - rMilli > rInterval){
   rMilli = currentMillis;
   Read();  
  }
  if(isMax)
    return;
  if(!isPlaying && currentMillis - bMilli > bInterval){
   bMilli = currentMillis;
   beep();   
  }
  if(isPlaying && currentMillis - pMilli > pulse){
   pMilli = currentMillis;   
   pause();
  }
  
}


void Read()
{
  // Read the ADC, and calculate voltage and resistance from it
  int flexADC = analogRead(FLEX_PIN);
  float flexV = flexADC * VCC / 1023.0;
  float flexR = R_DIV * (VCC / flexV - 1.0);

  // Use the calculated resistance to estimate the sensor's
  // bend angle:
  float angle = map(flexR, STRAIGHT_RESISTANCE, BEND_RESISTANCE, 0, 100.0);
  isPaused = angle < 15;
  if(rCounter = 100)
    rCounter = 0;
  if (angle != Angle) {
      Angle = angle;
      // only toggle the LED if the new button state is HIGH
      // change tone
      Measure(angle);
    }
  if ((millis() - lastDebounceTime) > debounceDelay && angle > 0) {
    // Send it to py
    Serial.println((int)angle);
    analogWrite(ledPin,flexV);
    // Serial.flush();
    // whatever the angle is at, it's been there for longer than the debounce
    // delay, so take it as the actual current state:
    // if the button state has changed:

     if (angle != oldAngle) {
        // reset the debouncing timer
        lastDebounceTime = millis();
      }
  }

  // save the angle. Next time through the loop, it'll be the oldAngle:
  oldAngle = angle;  
}

void Measure(float angle)
{
//  if(abs(oldAngle - angle) < 10)
//    return;
//  oldAngle = angle;
  duration = 150;  
  if(angle > 85)
  {
    pulse = 5;
    duration = 2000;
    tone(buzzer, 1200, 10
    000);
    isMax =  true;
  }
  else{    
    isMax =  false;
    if(angle > 80){
      pulse = 100;
    }
    else if(angle > 70){
      pulse = 200;
    }
    else if(angle > 60){
      pulse = 500;
    }
    else if(angle > 50){
      pulse = 650;
    }
    else if(angle > 40){
      pulse = 900;
    }
    else if(angle > 30){
      pulse = 1500;
    }
    else if(angle > 20){
      pulse = 2200;
    }
    else if(angle > 10){
      pulse = 3000;
    }
    else{
      pulse = 3500;
    }
  }
}
