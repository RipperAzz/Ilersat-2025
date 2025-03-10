#include <SPI.h>
#include <LoRa.h>

// 🎡 Definició dels pins de connexió LoRa
#define SS 18
#define RST 14
#define DIO0 26

void setup() {
    Serial.begin(115200);
    LoRa.setPins(SS, RST, DIO0);
   
    // 🎡 Inicialització del mòdul LoRa
    if (!LoRa.begin(868E6)) {
        Serial.println("❌ LoRa3: Error en iniciar LoRa!");
        while (1);
    }

    Serial.println("✅ LoRa3 preparat per rebre missatges.");
    Serial.println("📝 Escriu un missatge per enviar a LoRa1 (a través de LoRa2):");
}

void loop() {
    // 📥 Comprovació de missatges entrants
    int midaPaquet = LoRa.parsePacket();
    if (midaPaquet) {
        String rebut = "";
        while (LoRa.available()) {
            rebut += (char)LoRa.read();
        }

        Serial.print("📩 Missatge rebut: ");
        Serial.println(rebut);

        // 🔍 Buscar el separador '|' per identificar el destinatari
        int separador = rebut.indexOf('|');
        if (separador != -1) {
            String nodeDesti = rebut.substring(0, separador);
            String missatge = rebut.substring(separador + 1);

            // ✅ Només processar missatges que vinguin de LoRa2
            if (nodeDesti == "2") {
                Serial.print("💬 Missatge per a LoRa3: ");
                Serial.println(missatge);

                // 📡 Enviar resposta a LoRa1 a través de LoRa2 amb prefix "A"
                String resposta = "A|1|Rebut: " + missatge;
                Serial.print("📡 Enviant resposta: ");
                Serial.println(resposta);

                LoRa.beginPacket();
                LoRa.print(resposta);
                LoRa.endPacket();
            } else {
                Serial.println("⚠️ Missatge ignorat (no prové de LoRa2).");
            }
        }
    }

    // 📝 Permetre a l'usuari enviar missatges a LoRa1 a través de LoRa2 amb prefix "B"
    if (Serial.available()) {
        String missatge = Serial.readStringUntil('\n');
        missatge.trim(); // Eliminar espais en blanc sobrants
        if (missatge.length() > 0) {
            // 🔖 Afegir el prefix "B|2|" per indicar que LoRa2 ha de reenviar-ho
            String missatgePerEnviar = "B|2|" + missatge;

            // 📡 Enviar missatge a LoRa2
            LoRa.beginPacket();
            LoRa.print(missatgePerEnviar);
            LoRa.endPacket();

            Serial.print("📡 Enviat a LoRa2: ");
            Serial.println(missatgePerEnviar);
        }
    }
}
