#!/bin/bash

#build the sketch in ./src/scketch.ino
sudo ino clean
sudo ino build
#flash the arduino witch the scketch
sudo avrdude -p atmega328p -P /dev/ttyS0 -c arduino -b 115200 -D -U flash:w:.build/uno/firmware.hex:i -vv
