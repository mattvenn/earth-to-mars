#ifndef ETM_h
#define ETM_h

#include <SoftwareSerial.h>

/*
pin 1 of megaspi header is cloests to rst button
pin 1 = gnd
pin 3 = rx
pin 5 = +5v
*/

const byte rxPin = 11; 
const byte txPin = 12;

// set up a new serial object
SoftwareSerial rfid_serial (rxPin, txPin);

void setupETM() {
    // put your setup code here, to run once:
    rfid_serial.begin(9600);
}

String read_rfid()
{
	String rfid = "";
	if(rfid_serial.available() == 14)
	{
		//if not correct start bit, abort
		if(rfid_serial.read() != 0x02)
		{
			rfid_serial.flush();
			return rfid;
		}

		for( int i = 0; i < 12; i ++ )
			rfid += (char)rfid_serial.read();
		//discard end bit
		rfid_serial.read();
	}
	return rfid;
}

#endif
