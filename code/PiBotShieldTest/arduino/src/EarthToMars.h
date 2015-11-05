#ifndef ETM_h
#define ETM_h

#define H_SENSE A6
#define H_HEAT 11
#define DHT_PIN 12
#define DHTTYPE DHT11
#include "DHT.h"
DHT dht(DHT_PIN, DHTTYPE);

void setupETM() {
    // put your setup code here, to run once:
    dht.begin();
}

int read_temp()
{
    float temp = dht.readTemperature();
    return int(temp*10);
}

int read_humidity()
{
    float humidity = dht.readHumidity();
    return int(humidity*10);
}

int read_h2()
{
    //ramp up heater
    for(int i=0; i< 255; i++)
    {
        delay(5);
        analogWrite(H_HEAT,i);
    }
    delay(500);
    int h2 = analogRead(A6);
    //turn off heater
    analogWrite(H_HEAT,0);
    return h2;
}

#endif
