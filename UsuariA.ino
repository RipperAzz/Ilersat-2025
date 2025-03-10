#include <SPI.h>
#include <LoRa.h>

#define SS 18
#define RST 14
#define DIO0 26

void setup() {
    Serial.begin(115200);
    LoRa.setPins(SS, RST, DIO0);
    
    if (!LoRa.begin(868E6)) {
        Serial.println("❌ LoRa1: Error en iniciar LoRa!");
        while (1); // Atura el programa si hi ha un error en la inicialització
    }

    Serial.println("✅ LoRa1 preparat. Escriu un missatge per a LoRa3:");
}

void loop() {
    // 📤 ENVIAMENT de missatge a LoRa2
    if (Serial.available()) { // Comprova si hi ha entrada de l'usuari
        String missatge = Serial.readStringUntil('\n'); // Llegeix el missatge fins a salt de línia
        missatge.trim(); // Elimina espais en blanc sobrants

        if (missatge.length() > 0) { // Comprova que el missatge no estigui buit
            String paquet = "A|3|" + missatge;  // Afegim el prefix per indicar l'origen (A) i el destinatari (LoRa3)
            Serial.print("📡 Enviant a LoRa2: ");
            Serial.println(paquet);

            LoRa.beginPacket(); // Comença el paquet LoRa
            LoRa.print(paquet); // Escriu el missatge dins del paquet
            LoRa.endPacket(); // Finalitza i envia el paquet
            
            Serial.println("✅ Missatge enviat a LoRa2.");
            delay(100); // Petita pausa per evitar saturació
        }
    }

    // 📥 RECEPCIÓ de resposta de LoRa3
    int midaPaquet = LoRa.parsePacket(); // Comprova si ha arribat algun paquet
    if (midaPaquet) {
        String rebut = "";
        while (LoRa.available()) { // Llegeix el paquet rebut caràcter per caràcter
            rebut += (char)LoRa.read();
        }

        Serial.print("📩 Paquet rebut: ");
        Serial.println(rebut);

        int primerSeparador = rebut.indexOf('|'); // Busca el primer separador per identificar l'origen
        int segonSeparador = rebut.indexOf('|', primerSeparador + 1); // Busca el segon separador per identificar el destinatari
        
        if (primerSeparador != -1 && segonSeparador != -1) {
            String nodeOrigen = rebut.substring(0, primerSeparador); // Extreu l'origen
            String nodeDesti = rebut.substring(primerSeparador + 1, segonSeparador); // Extreu el destinatari
            String missatge = rebut.substring(segonSeparador + 1); // Extreu el contingut del missatge

            if (nodeDesti == "1") {  // Comprova si el missatge està destinat a LoRa1
                Serial.print("💬 Resposta rebuda de ");
                Serial.print(nodeOrigen);
                Serial.print(": ");
                Serial.println(missatge);
            }
        }
    }
}
