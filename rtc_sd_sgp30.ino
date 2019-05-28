// Date and time functions using a DS1307 RTC connected via I2C and Wire lib
#include <Wire.h>
#include <SD.h>
#include <SPI.h>

#include "RTClib.h"
#include "Adafruit_SGP30.h"

Adafruit_SGP30 sgp;

/* return absolute humidity [mg/m^3] with approximation formula
* @param temperature [°C]
* @param humidity [%RH]
*/
uint32_t getAbsoluteHumidity(float temperature, float humidity) {
    // approximation formula from Sensirion SGP30 Driver Integration chapter 3.15
    const float absoluteHumidity = 216.7f * ((humidity / 100.0f) * 6.112f * exp((17.62f * temperature) / (243.12f + temperature)) / (273.15f + temperature)); // [g/m^3]
    const uint32_t absoluteHumidityScaled = static_cast<uint32_t>(1000.0f * absoluteHumidity); // [mg/m^3]
    return absoluteHumidityScaled;
}

#if defined(ARDUINO_ARCH_SAMD)
// for Zero, output on USB Serial console, remove line below if using programming port to program the Zero!
   #define Serial SerialUSB
#endif

RTC_PCF8523 rtc;
const int chipSelect = 10;

void setup () {
  

#ifndef ESP8266
  while (!Serial); // for Leonardo/Micro/Zero
#endif

  Serial.begin(9600);
  if (! sgp.begin()){
    Serial.println("Sensor not found :(");
    while (1);
  }
  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1);
  }

  if (! rtc.initialized()) {
    Serial.println("RTC is NOT running!");
    // following line sets the RTC to the date & time this sketch was compiled
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    // This line sets the RTC with an explicit date & time, for example to set
    // January 21, 2014 at 3am you would call:
    // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
  }
  

   Serial.print("Initializing SD card...");

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    while (1);
  }
  Serial.println("card initialized.");
  File dataFile = SD.open("data.csv", FILE_WRITE);
  DateTime now = rtc.now();
  dataFile.println("0,");
  dataFile.print(now.unixtime());
}

void loop () {
  File dataFile = SD.open("data.csv", FILE_WRITE);
  if (! sgp.IAQmeasure()) {
    Serial.println("Measurement failed");
    return;
  }
    DateTime now = rtc.now();
    dataFile.print(sgp.eCO2);
    dataFile.print(",");
    dataFile.print(now.unixtime());
    dataFile.println();
    dataFile.close();
    Serial.println("data written");
    delay(100);
}
