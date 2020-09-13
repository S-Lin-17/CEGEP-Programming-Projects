// Pin numbers, variables who will always be constant (L for Left, M for Middle, R for Right)
const int ledPinL = 8;
const int ledPinR = 4;
const int buttonPinL = 12; 
const int buttonPinR = 2;
const int buttonPinM = 7;

// Initializing variables that can change 
int ledLState = LOW;
int ledRState = LOW;
int buttonLState;
int buttonRState;
int buttonMState;
int lastButtonLState = LOW;  //
int lastButtonRState = LOW;  // Previous reading from input pin (will be useful for debouncing)
int lastButtonMState = LOW;  //
int mButtonPressed = LOW;
int pinSelect;
unsigned int startTime = 0;     //
unsigned int endTime = 0;       // Will only store positive values
unsigned int reactionTime = 0;  //

int long ranDelay = 0; // Time is measured in milliseconds, variable may be long

// Debounce is needed to make sure that a button is definitely pressed;
// Without debounce, pressing a button once may cause unpredictable results
unsigned long lastDebounceTime = 0; // last time the output pin was toggled
unsigned long debounceDelay = 10; // means we only want to accept a sample that was taken at least 10ms
                                  // after last sample

int gameReset = 1;
int takeReading = LOW;

// Will help in reading button pins 
int readingL;
int readingM; 
int readingR;

void setup()
{
  Serial.begin(9600); // Opens serial port and sets data rate to 9600 bytes per second
  pinMode(ledPinL, OUTPUT);
  pinMode(ledPinR, OUTPUT);
  pinMode(buttonPinL, INPUT);
  pinMode(buttonPinR, INPUT);
  pinMode(buttonPinM, INPUT);

  // set initial LED state
  digitalWrite(ledPinL, ledLState);
  digitalWrite(ledPinR, ledRState);
}

void loop(){

  if(gameReset == 1)
  {
    Serial.println("Push the middle button to start the game.");
    gameReset = 0; // Like seen at the bottom of code, game resets when middle button is pressed, then returns LOW for game to stasrt
    takeReading = LOW; // No reading of left and right button
    // Time variables are reset
    startTime = 0;
    endTime = 0;
    lastDebounceTime = 0;
    reactionTime = 0;
  }

  if(mButtonPressed == HIGH)
  {
    digitalWrite(ledPinL, LOW);
    digitalWrite(ledPinR, LOW);
    pinSelect = random(1,3); // Chooses a random number, either 1 or 2, which determines the LED that's going to light up
    Serial.println("Press the button corresponding to the LED light as quickly as possible.");
    delay(1000);
    Serial.println("Get ready...");
    delay(1000);

    if(pinSelect == 1) // Left LED pin selected
    {
      ranDelay = random(5000); // Random delay between 1 and 6 seconds after the "Get ready..." quote
      delay(ranDelay);
      Serial.println("Go!");
      digitalWrite(ledPinL, HIGH); 
      digitalWrite(ledPinR, LOW);
      startTime = millis();
      ledLState == HIGH; // Setting these variables is important to verify
      ledRState == LOW;  // if user has pressed the right corresponding button to LED
    }

    else // Right LED pin selected instead
    {
      ranDelay = random(5000); // Random delay between 1 and 6 seconds after the "Get ready..." quote
      delay(ranDelay);
      Serial.println("Go!");
      digitalWrite(ledPinL, LOW);
      digitalWrite(ledPinR, HIGH);
      startTime = millis();
      ledLState == LOW; // Setting these variables is important to verify
      ledRState == HIGH;  // if user has pressed the right corresponding button to LED
    }
    mButtonPressed = LOW; // Will be set to HIGH towards the bottom of the code
  }

  readingM = digitalRead(buttonPinM); // reads middle button, returns HIGH or LOW

  if(takeReading == HIGH) 
  // as seen in bottom of code, takeReading returns HIGH when middle button is pressed
  {
    if (pinSelect == 1) // Left LED lights up
    {
      readingL = digitalRead(buttonPinL);
      readingR = digitalRead(buttonPinR);
    }
    if (pinSelect == 2) // Right LED lights up
    {
      readingR = digitalRead(buttonPinR);
      readingL = digitalRead(buttonPinL);
    }
  }

  // Check for how long any of the buttons have been activated 
  // (i.e. for how long the switch has changed), either by noise or by pressing
  if(readingL != lastButtonLState || readingM != lastButtonMState || readingR != lastButtonRState)
  {
    lastDebounceTime = millis(); 
    // Will always reset debouncing timer every time button has been pressed / activated by noise
  }

  if ((millis() - lastDebounceTime) > debounceDelay) // i.e. has enough time passed from the previous input
                                                     // for the new input to be legitimate (> 50ms)
  {
    if (readingL != buttonLState) // When readingL is HIGH and buttonLState is LOW
    {
      buttonLState = readingL; // becomes HIGH 

      if (buttonLState == HIGH && pinSelect == 1) // Executes the statement only if left button is pressed when left LED lights up
      {
        endTime = millis();
        Serial.print("Your reaction time is: ");
        reactionTime =(endTime - startTime);
        Serial.print(reactionTime);
        Serial.print("ms.");
        Serial.println();
        gameReset = 1; // Game resets and goes to beginning of loop when middle button is pushed
      }
      if (buttonLState == HIGH && pinSelect == 2) // If left button is pressed when right LED lighted up actually
      {
        Serial.println("Wrong button. Please pay attention next time.");
        gameReset = 1;
      }
    }
    if (readingR != buttonRState) // When readingR is HIGH and buttonRState is LOW
      {
      buttonRState = readingR; // becomes HIGH 

      if (buttonRState == HIGH && pinSelect == 2) // Executes the statement only if right button is pressed when right LED lights up
      {
        endTime = millis();
        Serial.print("Your reaction time is: ");
        reactionTime =(endTime - startTime);
        Serial.print(reactionTime);
        Serial.print("ms.");
        Serial.println();
        gameReset = 1; // Game resets and goes to beginning of loop when middle button is pushed
      }
      if (buttonRState == HIGH && pinSelect == 1) // If right button is pressed when left LED lighted up actually
      {
        Serial.println("Wrong button. Please pay attention next time.");
        gameReset = 1;
      }
      }

    if (readingM != buttonMState) // When middle button is pressed
     {
      buttonMState = readingM; // becomes HIGH

      if (buttonMState == HIGH)
      {
        mButtonPressed = HIGH; // Will return to beginning to loop to start new game
        takeReading = HIGH; 
      }
     }
    }

    // Saving the readings so that next time through loop they will be "lastButtonState"
    lastButtonLState = readingL;
    lastButtonRState = readingR;
    lastButtonMState = readingM;
    }
  
