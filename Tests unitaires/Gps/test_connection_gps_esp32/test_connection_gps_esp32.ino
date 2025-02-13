#include <TinyGPS++.h>
#include <HardwareSerial.h>

HardwareSerial gpsSerial(1);
TinyGPSPlus gps;

void setup() {
  Serial.begin(115200);
  gpsSerial.begin(9600, SERIAL_8N1, 13,15);
  Serial.println("Attente des données GPS...");
}

void loop() {
  while (gpsSerial.available()) {
    char c = gpsSerial.read();
    gps.encode(c);    // Envoi à TinyGPS++

    // Debug: Afficher chaque trame interprétée par TinyGPS++
    if (gps.satellites.isUpdated()) {
      Serial.print("Satellites détectés: ");
      Serial.println(gps.satellites.value());
    }

    if (gps.location.isUpdated()) {  // Vérifie si la position a été mise à jour
      Serial.println("\n---- Position Mise à Jour ----");
      Serial.print("Latitude: ");
      Serial.print(gps.location.lat(), 6);
      Serial.print(" | Longitude: ");
      Serial.print(gps.location.lng(), 6);
      Serial.println();
    }
  }
}
