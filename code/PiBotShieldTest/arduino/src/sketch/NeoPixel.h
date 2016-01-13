// NeoPixel Ring simple sketch (c) 2013 Shae Erisson
// released under the GPLv3 license to match the rest of the AdaFruit NeoPixel library
#ifndef NeoPixel_h
#define NeoPixel_h

#include <Adafruit_NeoPixel.h>
#include <avr/power.h>

// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1
#define PIN            3

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS      8

// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals.
// Note that for older NeoPixel strips you might need to change the third parameter--see the strandtest
// example for more information on possible values.
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setupNeoPixel() {
  pixels.begin(); // This initializes the NeoPixel library.
};

void clearNeoPixels(){
    for(int i=0;i<NUMPIXELS;i++)
    {
        pixels.setPixelColor(i, pixels.Color(0,0,0));
        pixels.show();
    }
};

void writeNeoPixel(int pixelNumber,int r, int g, int b)
{
    pixels.setPixelColor(pixelNumber, pixels.Color(r,g,b));
    pixels.show();
};

void test() {

  // For a set of NeoPixels the first NeoPixel is 0, second is 1, all the way up to the count of pixels minus one.

  for(int i=0;i<NUMPIXELS;i++){

    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(i, pixels.Color(100,100,0)); // Moderately bright green color.

    pixels.show(); // This sends the updated pixel color to the hardware.

    delay(1000); // Delay for a period of time (in milliseconds).

  }
};
#endif
