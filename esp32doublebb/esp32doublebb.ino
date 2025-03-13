#include <esp_now.h>
#include <WiFi.h>
#include <esp_timer.h>
#include <cmath> // Pour isnan et isinf

// Adresse MAC du récepteur (ESP32 distant)
uint8_t receiverAddress[] = {0xD4, 0x8C, 0x49, 0x57, 0xF9, 0x40};

// Structure pour envoyer les données
typedef struct struct_sensor {
    int analogValue; // Lecture brute sur GPIO 35
    float windSpeed; // Vitesse du vent en km/h
    char windDirection[3]; // Direction du vent en 2 caractères + null terminator
} struct_sensor;

struct_sensor sensorData;
esp_now_peer_info_t peerInfo;

const int analogPin = 35; // Broche ADC pour la lecture analogique
const int windPin = 4;    // Broche numérique pour la vitesse du vent

unsigned long lastPulseTime = 0;
int lastWindState = LOW;
float windSpeed = 0.0;
char lastKnownDirection[3] = "--";
esp_timer_handle_t timerHandle;

// Détermine la direction du vent en fonction de la valeur analogique
void determineWindDirection(int analogValue) {
    if (analogValue >= 180 && analogValue <= 250) strcpy(sensorData.windDirection, "E");
    else if (analogValue >= 2800 && analogValue <= 2900) strcpy(sensorData.windDirection, "N");
    else if (analogValue >= 3650 && analogValue <= 3750) strcpy(sensorData.windDirection, "W");
    else if (analogValue >= 800 && analogValue <= 1000) strcpy(sensorData.windDirection, "S");
    else if (analogValue >= 1500 && analogValue <= 1600) strcpy(sensorData.windDirection, "NE");
    else if (analogValue >= 3200 && analogValue <= 3350) strcpy(sensorData.windDirection, "NW");
    else if (analogValue >= 2050 && analogValue <= 2200) strcpy(sensorData.windDirection, "SW");
    else if (analogValue >= 500 && analogValue <= 600) strcpy(sensorData.windDirection, "SE");
    else strcpy(sensorData.windDirection, lastKnownDirection);
    
    strcpy(lastKnownDirection, sensorData.windDirection);
}

// Calcule la vitesse du vent en continu
void calculateWindSpeed() {
    int windState = digitalRead(windPin);
    if (windState == HIGH && lastWindState == LOW) {
        unsigned long currentTime = millis();
        if (lastPulseTime > 0) {
            float timeDiff = (currentTime - lastPulseTime) / 1000.0;
            if (timeDiff > 0) {
                windSpeed = 2.4 / timeDiff;
            } else {
                windSpeed = 0;
            }
        }
        lastPulseTime = currentTime;
    }
    lastWindState = windState;
    
    // Vérifier si la valeur est NaN ou infini, et la remplacer par 0
    if (isnan(windSpeed) || isinf(windSpeed)) {
        windSpeed = 0.0;
    }
    
    sensorData.windSpeed = windSpeed;
}

// Callback pour envoyer les données via interruption toutes les secondes
void sendDataCallback(void *arg) {
    sensorData.analogValue = analogRead(analogPin);
    determineWindDirection(sensorData.analogValue);
    
    esp_err_t result = esp_now_send(receiverAddress, (uint8_t *) &sensorData, sizeof(sensorData));
    
    Serial.printf("Valeur analogique (Pin 35) : %d\n", sensorData.analogValue);
    Serial.printf("Direction du vent : %s\n", sensorData.windDirection);
    Serial.printf("Vitesse du vent : %.2f km/h\n", sensorData.windSpeed);
    Serial.println(result == ESP_OK ? "Données envoyées avec succès" : "Erreur d'envoi");
}

void setup() {
    Serial.begin(115200);
    pinMode(analogPin, INPUT);
    pinMode(windPin, INPUT_PULLUP);

    WiFi.mode(WIFI_STA);

    if (esp_now_init() != ESP_OK) {
        Serial.println("Erreur d'initialisation ESP-NOW");
        return;
    }

    esp_now_register_send_cb(NULL);
    memcpy(peerInfo.peer_addr, receiverAddress, 6);
    peerInfo.channel = 0;
    peerInfo.encrypt = false;

    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
        Serial.println("Échec de l'ajout du pair");
        return;
    }

    // Configuration du timer pour exécuter sendDataCallback toutes les secondes
    const esp_timer_create_args_t timerArgs = {
        .callback = &sendDataCallback,
        .arg = NULL,
        .dispatch_method = ESP_TIMER_TASK,
        .name = "SendDataTimer"
    };
    esp_timer_create(&timerArgs, &timerHandle);
    esp_timer_start_periodic(timerHandle, 2000000); // 1 seconde
}

void loop() {
    calculateWindSpeed(); // Calcul en continu de la vitesse du vent
}
