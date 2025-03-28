import serial
import re
import threading
Thread_lock = threading.Lock()
sery = serial.Serial(port='COM5', baudrate=115200)
x = ""

def send_msg():
    global x
    while True:
        try:
            with open("C:/Users/zil08/OneDrive/Documents/Cansat-APP/ilernsat/outin_lora.csv", "r+") as data:
                Data = data.readlines()
                if len(Data) != x and len(Data) >= 1:
                    print(Data[-1])
                    x = len(Data)
                    sery.write(Data[-1].encode("utf-8"))
                else:
                    print("Hasta aqui")
                    continue
        except Exception:
            print("Archivo no creado [ESPERANDO]")
            continue

def recv_msg_background():
    while True:
        try:
            Data = sery.read().decode("utf-8", errors='ignore')
            Data = Data.replace("\n", "")
            if re.search("MENSAJE", Data):
                with open("C:/Users/zil08/OneDrive/Documents/Cansat-APP/ilernsat/grafic_output.csv", "+a") as data:
                    data.write(Data)
            else:
                with open("C:/Users/zil08/OneDrive/Documents/Cansat-APP/ilernsat/output.csv", "+a") as data:
                    data.write(Data)
        except Exception as e:
            print(f"Aviso:  {e}")
            continue

Thread_send = threading.Thread(target=send_msg, daemon=True)
Thread_recv = threading.Thread(target=recv_msg_background, daemon=True)

if __name__ == '__main__':
    Thread_send.start()
    Thread_recv.start()

    Thread_send.join()
    Thread_recv.join()