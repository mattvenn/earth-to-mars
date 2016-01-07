#ifndef ENCODERS_H
#define ENCODERS_H

#include "Encoder.h"

#define RIGHT_ENCODER_A A0//new A0// old A0  //prev A1
#define RIGHT_ENCODER_B 3// new 3//old A1  //prev A0
#define LEFT_ENCODER_A 4 //new 4 // old 4   //prev A7
#define LEFT_ENCODER_B 2// new 2 //old 7   //prev A6

long int countLeft;
long int countLeftNew;
long int countRight;
long int countRightNew;
boolean directionLeft;
boolean directionRight;
Encoder encRight(RIGHT_ENCODER_A,RIGHT_ENCODER_B);
Encoder encLeft(LEFT_ENCODER_A,LEFT_ENCODER_B);
  

void resetCount()
{
  directionLeft = 0;
  directionRight = 0;
  countLeft = 0;
  encLeft.write(0);
  countRight = 0;
  encRight.write(0);
};

void encodersInit()
{
  resetCount();
};

long int getLeftCount()
{
  countLeft = encLeft.read();  
  return countLeft;
};

long int getRightCount()
{
  countRight = encRight.read();  
  return countRight;
};

void setLeftCount(int val)
{
  encLeft.write(val);
};

void setRightCount(int val)
{
  encRight.write(val);
};

boolean getLeftDirection()
{
  countLeftNew =  encLeft.read();
  if(countLeftNew>countLeft){
  	directionLeft = true;	
  }
  else{
	directionLeft = false;
  }
  return directionLeft;
};

boolean getRightDirection()
{
  countRightNew =  encRight.read();
  if(countRightNew>countRight){
  	directionRight = true;	
  }
  else{
	directionRight = false;
  }
  return directionRight;
};

#endif
