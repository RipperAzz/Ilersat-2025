#include <TinyGPS++.h>
#include <TinyGPSPlus.h>
#include <SPI.h>
#include <LoRa.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <HardwareSerial.h>

// 📡 Pins LoRa
#define SS 18
#define RST 14
#define DIO0 26

// 📍 Configuració del GPS
static const int RXPin = 34, TXPin = 12;
static const uint32_t GPSBaud = 9600;

// 🔧 Creació d'objectes
Adafruit_BMP280 bmp;
TinyGPSPlus gps;
HardwareSerial gpsSerial(1);

void setup() {
    Serial.begin(115200);
    gpsSerial.begin(GPSBaud, SERIAL_8N1, RXPin, TXPin);
    Wire.begin();

    if (!bmp.begin(0x76)) {
        Serial.println("❌ No s'ha trobat el BMP280!");
        while (1);
    }

    // 📡 Configurar LoRa
    LoRa.setPins(SS, RST, DIO0);
    if (!LoRa.begin(868E6)) {
        Serial.println("❌ Error en iniciar LoRa!");
        while (1);
    }
    Serial.println("✅ LoRa2 Intermediari preparat.");
}

void loop() {
    // 📍 Llegir dades del GPS
    while (gpsSerial.available()) {
        gps.encode(gpsSerial.read());
    }

    if (gps.location.isValid()) {
        float lat = gps.location.lat();
        float lon = gps.location.lng();
        float alt = gps.altitude.meters();
        float temperatura = bmp.readTemperature();
        float pressio = bmp.readPressure() / 100.0;

        // 📡 Enviar dades del sensor a través de LoRa
        String sensorData = "B|2|GPS: " + String(lat, 6) + "," + String(lon, 6) +
                            " Alt: " + String(alt) +
                            " Temp: " + String(temperatura) +
                            " Pressió: " + String(pressio);

        LoRa.beginPacket();
        LoRa.print(sensorData);
        LoRa.endPacket();

        Serial.println("📡 Dades dels sensors enviades.");
    }

    // 📥 Reenviar missatges entre LoRa1 i LoRa3
    int midaPaquet = LoRa.parsePacket();
    if (midaPaquet) {
        String rebut = "";
        while (LoRa.available()) {
            rebut += (char)LoRa.read();
        }

        Serial.print("📩 Missatge rebut: ");
        Serial.println(rebut);

        int primerSeparador = rebut.indexOf('|');
        int segonSeparador = rebut.indexOf('|', primerSeparador + 1);

        if (primerSeparador != -1 && segonSeparador != -1) {
            String nodeOrigen = rebut.substring(0, primerSeparador);
            String nodeDesti = rebut.substring(primerSeparador + 1, segonSeparador);

            Serial.println("📡 Reenviant missatge...");
            LoRa.beginPacket();
            LoRa.print(rebut);
            LoRa.endPacket();
        }
    }
    delay(2000);
}
