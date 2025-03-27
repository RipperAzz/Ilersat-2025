import serial
import threading
import time

sery = serial.Serial(port='COM5', baudrate=115200)
lock = threading.Lock()
x = ""
def send_msg():
    global x
    while True:
        try:
            with open("C:/Users/zil08/OneDrive/Documents/Cansat-APP/ilernsat/outin_lora.csv") as data:
                Data = data.readlines()
                if len(Data) == x:
                    print("Espera datos")
                else:
                    print(Data[-1])
                    x = len(Data)
                    sery.write(Data[-2].encode("utf-8"))
        except FileNotFoundError:
            print("Arcivo no crado [ESPERANDO]")
        time.sleep(0.5)

def recv_msg_background():
    while True:
        try:
            with lock:
                Data = sery.read().decode("utf-8", errors='ignore')
            if Data:
                with open("C:/Users/zil08/OneDrive/Documents/Cansat-APP/lora_output.csv", "a", encoding="utf-8") as req:
                    req.write(Data)
        except Exception as e:
            print(f"[ERROR al recibir]")
            break

Thread1 = threading.Thread(target=recv_msg_background, daemon=True)
Thread2 = threading.Thread(target=send_msg, daemon=True)

if __name__ == '__main__':
    Thread1.start()
    Thread2.start()
    Thread1.join()
    Thread2.join()