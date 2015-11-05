#ifndef ENCODERS_H
#define ENCODERS_H

#include <PinChangeInt.h>

#define RIGHT_ENCODER_A A1
#define RIGHT_ENCODER_B A0
#define LEFT_ENCODER_A A7
#define LEFT_ENCODER_B A6

long int countLeft;
long int countRight;
boolean directionLeft;
boolean directionRight;

void resetCount()
{
  directionLeft = 0;
  directionRight = 0;
  countLeft = 0;
  countRight = 0;
};

void pulseInterrupt()
{
  int interruptedPin = PCintPort::arduinoPin;
  if(interruptedPin == LEFT_ENCODER_A)
  {
    countLeft++;
    if(digitalRead(LEFT_ENCODER_B))
      directionLeft=1;
    else
      directionLeft=0;
  }
  else if(interruptedPin == RIGHT_ENCODER_A)
  {
    countRight++;
    if(digitalRead(RIGHT_ENCODER_B))
      directionRight=1;
    else
      directionRight=0;
  }
};

void encodersInit()
{
  pinMode(RIGHT_ENCODER_B, INPUT);
  pinMode(RIGHT_ENCODER_A, INPUT);
  digitalWrite(RIGHT_ENCODER_A, HIGH); //trun on the pull-up resistor
  PCintPort::attachInterrupt(RIGHT_ENCODER_A,&pulseInterrupt, CHANGE);
  pinMode(LEFT_ENCODER_B, INPUT);
  pinMode(LEFT_ENCODER_A, INPUT);
  digitalWrite(LEFT_ENCODER_A, HIGH); //trun on the pull-up resistor
  PCintPort::attachInterrupt(LEFT_ENCODER_A,&pulseInterrupt, CHANGE);
  resetCount();
};

long int getLeftCount()
{
  return countLeft;
};

long int getRightCount()
{
  return countRight;
};

boolean getLeftDirection()
{
  return directionLeft;
};

boolean getRightDirection()
{
  return directionRight;
};

#endif
