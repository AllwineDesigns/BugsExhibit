#include "FastLED.h"
#define NUM_LEDS 64
CRGB leds[NUM_LEDS];
uint8_t noise[NUM_LEDS];
uint16_t t = 0;
uint16_t speed = 10;

CRGB color = {255,255,255};
unsigned long flashTime = 500;
unsigned long flashes = 3;
float dim = .7;
unsigned long lastFlash = 0;

static uint16_t x;
static uint16_t y;
static uint16_t z;

static uint16_t scale = 4;

void setup() { 
  // Create LEDs
  FastLED.addLeds<NEOPIXEL, 12>(leds, NUM_LEDS);

  // Set brightness
//  LEDS.setBrightness(50);

  // Turn off all LEDs
  for(int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::Black;
  }
  LEDS.show();

  // Initialize serial communication with Pi
  Serial.begin(9600);

  // Initialize some variables
  lastFlash = millis();
  x = random16();
  y = random16();
  z = random16();
}

void fillnoise8() {
  // generate noise value for every LED
  for(uint16_t i = 0; i < NUM_LEDS; i++) {
    float r = scale*(float)(i/8)/8;
    float c = scale*(float)(i%8)/8;
    uint8_t n = inoise8(r*(1 << 8)+x,c*(1 << 8)+y,z+t);

    float normN = (float)n/255;
    float gamma = 255*normN*normN;
    noise[i] = gamma;
  }
  t += speed;
}

void loop() {
  fillnoise8();

  // Time since we started flashing
  unsigned long curTime = millis()-lastFlash;

  // Current flash
  int curFlash = (float)curTime/flashTime;

  // If we're not done flashing
  if(curTime < flashTime*flashes) {
    // calculate the intensity of our flash 
    float intensity = pow(dim, curFlash)*fabs(sin((float)curTime/flashTime*PI));

    // set the color of each LED using the current color and flash intensity
    for (uint16_t i = 0; i < NUM_LEDS; i++) {
      CRGB curColor = color;
      float ledIntensity = intensity-((float)noise[i]/255);
      if(ledIntensity < 0) {
        ledIntensity = 0;
      }
      curColor.r *= ledIntensity;
      curColor.g *= ledIntensity;
      curColor.b *= ledIntensity;
      leds[i] = curColor;
    }
  } else {
    // otherwise, we're done flashing and want to turn off all LEDs
    for (uint16_t i = 0; i < NUM_LEDS; i++)
    {
      leds[i] = CRGB(0,0,0);
    }
  }

  // Serial message
  // r g b flashes flashTime(2bytes) speed
  if(Serial.available() >= 7) {
    lastFlash = millis();
    x = random16();
    y = random16();
    z = random16(); 

    scale = random8()%4+1;

    color.r = Serial.read();
    color.g = Serial.read();
    color.b = Serial.read();

    flashes = Serial.read();
    flashTime = Serial.read() << 8 | Serial.read();
    speed = Serial.read();
  }
  FastLED.show(); 
  delay(10);
}
