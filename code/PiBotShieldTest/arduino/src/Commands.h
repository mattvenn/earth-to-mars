#ifndef COMMANDS_H
#define COMMANDS_H

#include "Arduino.h"
#include "Ultrasound.h"

typedef enum
  {
    READ_DIGIATL
  , READ_ANALOG
  , WRITE_DIGITAL
  , WRITE_PWM
  , READ_ULTRASOUND
  , READ_LEFT_ENCODER
  , READ_RIGHT_ENCODER
  , WRITE_NEO_PIXEL
  , RESET_NEO_PIXELS
  , READ_TEMP
  , READ_H2
  , READ_HUMIDITY
  } Commands;

int readDigital(int pin)
{
  pinMode(pin, INPUT);
  return digitalRead(pin);
};

int readAnalog(int pin)
{
  pinMode(pin, INPUT);
  return analogRead(pin);
};

void writeDigital(int pin,int value)
{
  pinMode(pin, OUTPUT);
  digitalWrite(pin,value==1.0);
};

void writePWM(int pin,int value)
{
  pinMode(pin, OUTPUT);
  analogWrite(pin,value);
};

#endif
