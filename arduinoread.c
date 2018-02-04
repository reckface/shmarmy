int led1 = 5;
int led2 = 6;
int motion = 3;
int wait = 1500; //500ms = 1/2s
 

int potPin = 0;    // select the input pin for the potentiometer
int ledPin = 13;   // select the pin for the LED
int val = 0;       // variable to store the value coming from the sensor

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  if (Serial.available() > 0)
  {
    int pyVal = Serial.read();
    int potVal = analogRead(potPin);
    val = potVal / 11; //map(potVal, 700, 900, 0, 255);
    Serial.write(val);
    analogWrite(ledPin, val);
    delay(100);
  }
}