 #include <TinyGPSPlus.h>
#include <SomeSerial.h>  // Remplace SoftwareSerial

#define RXPin 4  // GPS TX → Arduino RX
#define TXPin 3  // GPS RX → Arduino TX
#define GPSBaud 9600  // Vitesse par défaut du GPS

SomeSerial gpsSerial(RXPin, TXPin);
TinyGPSPlus gps;

void setup() {
  Serial.begin(115200); // Moniteur série pour voir les données GPS
  gpsSerial.begin(GPSBaud);
  Serial.println("Initialisation GPS...");
}

void loop() {
  while (gpsSerial.available() > 0) {
    Serial.println("test");
    gps.encode(gpsSerial.read());

    if (gps.location.isUpdated()) {
      Serial.print("Latitude: ");
      Serial.print(gps.location.lat(), 6);
      Serial.print(" | Longitude: ");
      Serial.print(gps.location.lng(), 6);
      Serial.println();
    }
  }
}
