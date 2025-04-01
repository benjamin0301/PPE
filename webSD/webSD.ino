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
#include <SD.h>
#include <SPI.h>

// Initialisation des capteurs
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28, &Wire);
HardwareSerial gpsSerial(1);
TinyGPSPlus gps;

// EEPROM avec Preferences (conservée mais non utilisée pour l'enregistrement)
Preferences preferences;

// Initialisation du serveur Web
WebServer server(80);

// Variable indiquant si le serveur web est actif
bool webServerActive = false;

// Structure des données reçues via ESP-NOW
struct ReceivedData {
  int analogValue;
  float windSpeed;
  char windDirection[3];
};

ReceivedData receivedWindData = {0, 0.0, "--"}; // Valeurs par défaut

// Variables globales pour l'enregistrement sur carte SD
bool recording = false;           // true pendant l'enregistrement
unsigned long lastRecordTime = 0; // Pour prendre une mesure toutes les secondes
File dataFile;                    // Fichier ouvert sur la carte SD
bool fileOpen = false;            // Indique si le fichier est ouvert
bool firstRecordWritten = false;  // Pour gérer la virgule entre objets JSON
String currentFilename = "";      // Nom du fichier en cours d'enregistrement

// Anti-rebond sur le bouton (1 seconde)
unsigned long lastDebounceTime = 0;
const unsigned long debounceDelay = 1000;  // 1 seconde
bool lastButtonState = LOW;

// Pins de contrôle
const int startPin = 17; // Démarre/arrête l'enregistrement
const int wifiPin = 4;   // Active le serveur Web
const int SD_CS = 5;     // Chip select de la carte SD

// Callback pour la réception de données via ESP-NOW
void OnDataRecv(const esp_now_recv_info_t *info, const uint8_t *incomingData, int len) {
  // Mise à jour des données reçues uniquement si le serveur web n'est pas actif
  if (!webServerActive) {
    memcpy(&receivedWindData, incomingData, sizeof(receivedWindData));
  }
}

// 📌 Page d'accueil : affiche tous les fichiers "nav*.json" enregistrés sur la carte SD
void handleRoot() {
  String html = "<html><head><title>ESP32 Data Server</title></head><body>";
  html += "<h2>Fichiers enregistrés</h2>";

  Serial.println("handleRoot() appelé : tentative d'ouverture du répertoire racine");
  File root = SD.open("/");
  if (!root) {
    Serial.println("Erreur : Impossible d'ouvrir le répertoire racine de la SD");
    html += "<p>Impossible d'ouvrir le répertoire racine.</p>";
  } else {
    Serial.println("Répertoire racine ouvert avec succès");
    
    // Affichage de tous les fichiers pour debug
    File debugFile = root.openNextFile();
    while (debugFile) {
      Serial.print("Fichier trouvé : ");
      Serial.println(debugFile.name());
      debugFile.close();
      debugFile = root.openNextFile();
    }
    root.rewindDirectory(); // Réinitialise l'itérateur pour la recherche suivante

    bool fileFound = false;
    File file = root.openNextFile();
    while (file) {
      String filename = file.name();
      Serial.print("---------");
      Serial.println(filename);
      // Vérifier si le nom commence par "nav" et se termine par ".json"
      if (filename.startsWith("nav") && filename.endsWith(".json")) {
        fileFound = true;
        // Ajout d'un lien pour télécharger le fichier
        html += "<p><a href='/download?file=" + filename + "' download>" + filename + "</a></p>";
      }
      file.close();
      file = root.openNextFile();
    }
    root.close();

    if (!fileFound) {
      html += "<p>Aucun fichier trouvé.</p>";
    }
  }
  
  html += "</body></html>";
  server.send(200, "text/html", html);
}

// 📌 Téléchargement d'un fichier JSON via le paramètre "file"
void handleDownload() {
  if (!server.hasArg("file")) {
    server.send(400, "text/plain", "Paramètre 'file' manquant.");
    return;
  }
  String requestedFile = server.arg("file");
  if (!requestedFile.startsWith("/")) {
    requestedFile = "/" + requestedFile;
  }
  File file = SD.open(requestedFile, FILE_READ);
  if (!file) {
    server.send(404, "text/plain", "Fichier non trouvé.");
    return;
  }
  // Préparation du nom pour le téléchargement (sans le '/')
  String downloadName = requestedFile;
  if (downloadName.startsWith("/"))
    downloadName = downloadName.substring(1);

  server.sendHeader("Content-Type", "application/json");
  server.sendHeader("Content-Disposition", "attachment; filename=" + downloadName);
  server.streamFile(file, "application/json");
  file.close();
  Serial.print("📡 Fichier envoyé : ");
  Serial.println(requestedFile);
}

// 📌 Démarrage du serveur Web
void startWebServer() {
  Serial.println("✅ Activation du serveur Web...");
  WiFi.mode(WIFI_AP);
  WiFi.softAP("DataServer");

  // Réinitialiser la carte SD après le démarrage du mode AP
  if (!SD.begin(SD_CS)) {
    Serial.println("Échec de la réinitialisation de la carte SD après démarrage du WiFi AP!");
  } else {
    Serial.println("Carte SD réinitialisée avec succès après démarrage du WiFi AP.");
  }

  // Définition des routes
  server.on("/", handleRoot);
  server.on("/download", handleDownload);
  server.begin();
  webServerActive = true; // Indiquer que le serveur est actif

  // Désactiver ESP-NOW pour libérer les ressources Wi-Fi
  esp_now_deinit();

  Serial.println("🌐 Serveur web démarré ! Connectez-vous au réseau 'DataServer'.");
}

// Fonction pour déterminer le prochain nom de fichier disponible sur la carte SD (extension .json)
String getNextFilename() {
  int fileNum = 1;
  String filename;
  do {
    filename = "/nav" + String(fileNum) + ".json";
    fileNum++;
  } while (SD.exists(filename));
  return filename;
}

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);

  pinMode(startPin, INPUT_PULLDOWN);
  pinMode(wifiPin, INPUT_PULLDOWN);

  // Initialisation du BNO055
  if (!bno.begin()) {
    Serial.println("Erreur d'initialisation du BNO055 !");
    while (1);
  }

  // Initialisation du mode station pour ESP-NOW
  WiFi.mode(WIFI_STA);

  // Initialisation d'ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Erreur d'initialisation d'ESP-NOW !");
    return;
  }
  esp_now_register_recv_cb(OnDataRecv);

  // Initialisation du GPS
  gpsSerial.begin(9600, SERIAL_8N1, 13, 15);

  // Initialisation de l'EEPROM (conservée)
  preferences.begin("data_log", false);

  // Initialisation de la carte SD
  if (!SD.begin(SD_CS)) {
    Serial.println("Échec de l'initialisation de la carte SD !");
  } else {
    Serial.println("Carte SD initialisée.");
  }
}

void loop() {
  // Gestion du bouton de démarrage/arrêt avec anti-rebond (1 seconde)
  bool reading = digitalRead(startPin);
  if (reading == HIGH && lastButtonState == LOW && (millis() - lastDebounceTime > debounceDelay)) {
    lastDebounceTime = millis();
    if (!recording) {
      // Démarrer l'enregistrement
      recording = true;
      lastRecordTime = millis();
      firstRecordWritten = false;
      currentFilename = getNextFilename();
      dataFile = SD.open(currentFilename, FILE_WRITE);
      if (dataFile) {
        dataFile.print("[");  // Début d'un tableau JSON
        fileOpen = true;
        Serial.print("✅ Démarrage de l'enregistrement dans le fichier ");
        Serial.println(currentFilename);
      } else {
        Serial.println("Erreur lors de l'ouverture du fichier sur la carte SD !");
        recording = false;
      }
    } else {
      // Arrêter l'enregistrement
      recording = false;
      if (fileOpen) {
        dataFile.println("]"); // Fin du tableau JSON
        dataFile.close();
        fileOpen = false;
        Serial.println("🛑 Enregistrement arrêté et fichier sauvegardé sur la carte SD.");
      }
    }
  }
  lastButtonState = reading;

  // Activation du serveur Web si le bouton sur wifiPin est pressé et si le serveur n'est pas déjà actif
  if (digitalRead(wifiPin) == HIGH && !webServerActive) {
    startWebServer();
  }

  // Pendant l'enregistrement, prise d'une mesure toutes les secondes
  if (recording) {
    unsigned long currentMillis = millis();
    if (currentMillis - lastRecordTime >= 1000) {
      lastRecordTime = currentMillis;

      // Lecture des capteurs BNO055
      sensors_event_t event, accel, gyro;
      bno.getEvent(&event, Adafruit_BNO055::VECTOR_EULER);
      bno.getEvent(&accel, Adafruit_BNO055::VECTOR_ACCELEROMETER);
      bno.getEvent(&gyro, Adafruit_BNO055::VECTOR_GYROSCOPE);

      // Récupérer le timestamp (en secondes)
      uint32_t timestamp = millis() / 1000;

      // Lecture du GPS
      while (gpsSerial.available()) {
        gps.encode(gpsSerial.read());
      }
      double latitude = gps.location.isValid() ? gps.location.lat() : 0.0;
      double longitude = gps.location.isValid() ? gps.location.lng() : 0.0;

      // Construction de l'objet JSON pour cette mesure
      String recordStr = "";
      recordStr += "{";
      recordStr += "\"time\":" + String(timestamp) + ",";
      recordStr += "\"yaw\":" + String(event.orientation.x) + ",";
      recordStr += "\"pitch\":" + String(event.orientation.y) + ",";
      recordStr += "\"roll\":" + String(event.orientation.z) + ",";
      recordStr += "\"lat\":" + String(latitude, 6) + ",";
      recordStr += "\"lon\":" + String(longitude, 6) + ",";
      recordStr += "\"windSpeed\":" + String(receivedWindData.windSpeed / 3.6) + ",";
      recordStr += "\"windDir\":\"" + String(receivedWindData.windDirection) + "\"";
      recordStr += "}";

      // Écriture de la mesure dans le fichier SD
      if (fileOpen) {
        if (firstRecordWritten) {
          dataFile.print(","); // Séparation par une virgule
        }
        dataFile.print(recordStr);
        dataFile.flush();  // Forcer l'écriture sur la carte SD
        firstRecordWritten = true;
        Serial.println("Enregistrement d'une nouvelle mesure...");
      }
    }
  }

  // Gestion du serveur Web si activé
  if (webServerActive) {
    server.handleClient();
  }
}
