#include <esp_now.h>
#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <TinyGPS++.h>
#include <HardwareSerial.h>
#include <Preferences.h>
#include <WebServer.h>

// Initialisation des capteurs
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28, &Wire);
HardwareSerial gpsSerial(1);
TinyGPSPlus gps;

// EEPROM avec Preferences
Preferences preferences;

// Initialisation du serveur Web
WebServer server(80);

// Structure des données enregistrées
struct DataRecord {
    uint32_t timestamp;
    float yaw, pitch, roll;
    float accelX, accelY, accelZ;
    float gyroX, gyroY, gyroZ;
    float temperature;
    double latitude, longitude;
    float windSpeed;
    char windDirection[3];
};

// Adresse MAC de l’émetteur (autre ESP32)
uint8_t broadcastAddress[] = {0xD4, 0x8C, 0x49, 0x57, 0xF9, 0x40};

// Variables globales
bool recording = false;
bool recordingDone = false;
bool webServerActive = false;
DataRecord records[10]; // Stockage des 10 secondes de données
int recordIndex = 0;
unsigned long lastRecordTime = 0;
int fileIndex = 1; // Pour incrémenter le nom des fichiers

// Structure des données reçues via ESP-NOW
struct ReceivedData {
    int analogValue;
    float windSpeed;
    char windDirection[3];
};

ReceivedData receivedWindData = {0, 0.0, "--"}; // Valeurs par défaut

// Pins de contrôle
const int startPin = 17; // Démarre l'enregistrement
const int wifiPin = 4;   // Active le serveur Web

// Callback pour la réception de données via ESP-NOW
void OnDataRecv(const esp_now_recv_info_t *info, const uint8_t *incomingData, int len) {
    if (!webServerActive) { // Désactiver ESP-NOW lorsque le serveur web est actif
        memcpy(&receivedWindData, incomingData, sizeof(receivedWindData));
    }
}

// 📌 Page d'accueil du serveur Web
void handleRoot() {
    String html = "<html><head><title>ESP32 Data Server</title></head><body>";
    html += "<h2>Bienvenue sur l'ESP32 Data Server</h2>";
    html += "<p><a href='/download' download='data.json'>📥 Télécharger les données enregistrées</a></p>";
    html += "</body></html>";

    server.send(200, "text/html", html);
}

// 📌 Génération et envoi du fichier JSON
void handleDownload() {
    String json = "[";
    for (int i = 0; i < 10; i++) {
        json += "{";
        json += "\"time\":" + String(records[i].timestamp) + ",";
        json += "\"yaw\":" + String(records[i].yaw) + ",";
        json += "\"pitch\":" + String(records[i].pitch) + ",";
        json += "\"roll\":" + String(records[i].roll) + ",";
        json += "\"lat\":" + String(records[i].latitude, 6) + ",";
        json += "\"lon\":" + String(records[i].longitude, 6) + ",";
        json += "\"windSpeed\":" + String(records[i].windSpeed) + ",";
        json += "\"windDir\":\"" + String(records[i].windDirection) + "\"";
        json += "}";
        if (i < 9) json += ",";
    }
    json += "]";

    server.sendHeader("Content-Disposition", "attachment; filename=data.json");
    server.send(200, "application/json", json);
    Serial.println("📡 Fichier JSON envoyé !");
}

// 📌 Démarrage du serveur Web
void startWebServer() {
    Serial.println("✅ Activation du serveur Web...");
    WiFi.mode(WIFI_AP);
    WiFi.softAP("DataServer");

    // Routes
    server.on("/", handleRoot);
    server.on("/download", handleDownload);
    server.begin();
    webServerActive = true;

    // Désactiver ESP-NOW
    esp_now_deinit();

    Serial.println("🌐 Serveur web démarré ! Connectez-vous au réseau 'DataServer'.");
}

void setup() {
    Serial.begin(115200);
    while (!Serial) delay(10);

    pinMode(startPin, INPUT_PULLDOWN);
    pinMode(wifiPin, INPUT_PULLDOWN);

    // Initialisation du BNO055
    if (!bno.begin()) {
        while (1);
    }

    // Initialisation du mode station pour ESP-NOW
    WiFi.mode(WIFI_STA);

    // Initialisation d'ESP-NOW
    if (esp_now_init() != ESP_OK) {
        return;
    }
    esp_now_register_recv_cb(OnDataRecv);

    // Initialisation du GPS
    gpsSerial.begin(9600, SERIAL_8N1, 13, 15);

    // Initialisation de l'EEPROM
    preferences.begin("data_log", false);
}

void loop() {
    // Déclencher l'enregistrement si le bouton sur pin 18 est pressé
    if (digitalRead(startPin) == HIGH) {
        recording = true;
        lastRecordTime = millis();
        Serial.println("✅ Démarrage de l'enregistrement !");
    }

    // Activer le serveur Web si le bouton sur pin 5 est pressé
    if (digitalRead(wifiPin) == HIGH && !webServerActive) {
        startWebServer();
    }

    // Vérifier si l'enregistrement est en cours et qu'il ne s'est pas terminé
    if (recording && recordIndex < 10) {
        unsigned long currentMillis = millis();
        if (currentMillis - lastRecordTime >= 1000) {
            lastRecordTime = currentMillis;

            // Lecture des données BNO055
            sensors_event_t event, accel, gyro;
            bno.getEvent(&event, Adafruit_BNO055::VECTOR_EULER);
            bno.getEvent(&accel, Adafruit_BNO055::VECTOR_ACCELEROMETER);
            bno.getEvent(&gyro, Adafruit_BNO055::VECTOR_GYROSCOPE);

            // Récupérer le timestamp
            uint32_t timestamp = millis() / 1000;

            // Lecture GPS
            while (gpsSerial.available()) gps.encode(gpsSerial.read());

            double latitude = gps.location.isValid() ? gps.location.lat() : 0.0;
            double longitude = gps.location.isValid() ? gps.location.lng() : 0.0;

            // Stocker les données
            records[recordIndex] = {timestamp, event.orientation.x, event.orientation.y, event.orientation.z,
                                    accel.acceleration.x, accel.acceleration.y, accel.acceleration.z,
                                    gyro.gyro.x, gyro.gyro.y, gyro.gyro.z, bno.getTemp(),
                                    latitude, longitude, receivedWindData.windSpeed / 3.6,
                                    "--"};
            strcpy(records[recordIndex].windDirection, receivedWindData.windDirection);

            recordIndex++;
        }
    }

    // Sauvegarde et affichage des données après 10 secondes
    if (recordIndex == 10 && !recordingDone) {
        Serial.println("\n✅ Enregistrement terminé !");
        preferences.putBytes("records", records, sizeof(records));
        recordingDone = true;
    }

    // Gestion du serveur Web si activé
    if (webServerActive) {
        server.handleClient();
    }
}