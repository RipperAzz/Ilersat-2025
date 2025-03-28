import socket
import threading
import time
import re
clients = []
listener = None
socket_thread = None
running = False
IP = "0.0.0.0"
PORT = 4444
x = ""

def handler_client(client):
    while True:
        try:
            msg = client.recv(4096)
            if not msg:
                    break
            elif msg.decode(errors='ignore') == "Request__to__exit__server for Client [EXIT]":
                    client.close()
                    print(f"Se cerro conexion con | {client}")
            SMS = f"{msg.decode(errors='ignore')} => {time.ctime(time.time())}\n"
            with open("C:/Users/zil08/OneDrive/Documents/Cansat-APP/ilernsat/outin_lora.txt", "+a") as f:
                f.write(SMS)
        except:
            break
    client.close()
    if client in clients:
        clients.remove(client)

def send_message(msg):
    SMS = f"{msg} => {time.ctime(time.time())}\n"
    with open("C:/Users/zil08/OneDrive/Documents/Cansat-APP/ilernsat/outin_lora.txt", "a") as f:
        f.write(SMS)
    for c in clients:
        c.sendall(SMS.encode("ascii", errors='ignore'))

def handler_lora():
    global x 
    while True:
        try:
            with open("C:/Users/zil08/OneDrive/Documents/Cansat-APP/ilernsat/output.txt", "r+") as data:
                Data = data.readlines()
                if re.search("U2", Data[-2]):
                    for c in clients:
                        c.sendall(Data[-2].encode(errors="ignore"))

                    x = len(Data)
                
                else:
                    continue
        except Exception:
            continue
        time.sleep(0.3)
            
def recive_connection():
    global listener
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind((IP, PORT))
    listener.listen()
    print(f"[SOCKET] Escuchando en {IP}:{PORT}")
    while running:
        try:
            client, addr = listener.accept()
            clients.append(client)
            print(f"Cliente conectado: {addr}")
            threading.Thread(target=handler_client, args=(client,), daemon=True).start()
        except:
            break
            
def start_socket_server():
    global running, socket_thread
    running = True
    socket_thread = threading.Thread(target=recive_connection, daemon=True)
    lora_thread = threading.Thread(target=handler_lora, daemon=True)
    socket_thread.start()
    lora_thread.start()

def stop_socket_server():
    global running
    running = False
    print("Se cerro conexion")
    try:
        if listener:
            listener.close()
        for client in clients:
            client.close()
    except Exception as e:
        print(f"[ERROR] Cerrando servidor socket: {e}")