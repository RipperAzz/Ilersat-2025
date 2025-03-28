import serial
import threading
import re
import time
Thread_lock = threading.Lock()
sery = serial.Serial(port='COM5', baudrate=115200)
x = ""

def send_msg():
    global x
    while True:
        try:
            with open("C:/Users/zil08/OneDrive/Documents/Cansat-APP/ilernsat/outin_lora.txt") as data:
                Data = data.readlines()
                if len(Data) != x and len(Data) >= 1:
                    print(Data[-1])
                    x = len(Data)
                    sery.write(Data[-1].encode("utf-8"))
        except Exception:
            continue
        time.sleep(0.5)

def recv_msg_background():
    while True:
        try:
            with Thread_lock:
                Data = sery.read().decode("utf-8", errors='ignore')
                Data = Data.replace("\n", "")
                with open("C:/Users/zil08/OneDrive/Documents/Cansat-APP/ilernsat/output.txt", "a") as data:
                    data.write(Data)
        except Exception as e:
            print(f"Aviso:  {e}")
            break


Thread1 = threading.Thread(target=recv_msg_background, daemon=True)
Thread2 = threading.Thread(target=send_msg, daemon=True)

if __name__ == '__main__':
    Thread1.start()
    Thread2.start()
    Thread1.join()
    Thread2.join()