#ifndef ULTRASOUND_H
#define ULTRASOUND_H

#include "Arduino.h"

int readUltrasound(int triggerPin)
{
  pinMode(triggerPin, OUTPUT);
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(4);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  pinMode(triggerPin, INPUT);
  long duration = pulseIn(triggerPin, HIGH, 100000);//0.1 second of timeout
  long distance = (duration/2) / 29.1; //distance in cm

  return distance;
};

#endif

