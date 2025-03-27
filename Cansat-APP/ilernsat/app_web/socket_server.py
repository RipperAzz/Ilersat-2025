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

def handler_message(client):
    while running:
        try:
            msg = client.recv(1024)
            if not msg:
                break
            elif msg.decode('ascii', errors='ignore') == "Request__to__exit__server for Client [EXIT]":
                client.close()
                print(f"Se cerro conexion con {client}")
            SMS = f"{msg.decode('ascii', errors='ignore')} => {time.ctime(time.time())}"
            with open("C:/Users/zil08/OneDrive/Documents/Cansat-APP/ilernsat/outin_lora.csv", "a") as mobile_input:
                mobile_input.write(SMS + "/n")
            print(SMS)
        except:
            break
        time.sleep(0.5)
    client.close()
    if client in clients:
        clients.remove(client)

def send_message(msg):
    SMS = f"{msg} => {time.ctime(time.time())}"
    with open("C:/Users/zil08/OneDrive/Documents/Cansat-APP/ilernsat/outin_lora.csv", "a") as f:
        f.write(SMS + "/n")
    for c in clients:
        c.sendall(SMS.encode("ascii", errors='ignore'))

def send_lora_msg():
    global x
    while True:
        try:
            with open("C:/Users/zil08/OneDrive/Documents/Cansat-APP/lora_output.csv") as lora_recv:
                Data = lora_recv.readlines()
                if re.search("U2", Data[-3]):
                    if len(Data) != x:
                        print(Data[-3])
                        x = len(Data)
                        for c in clients:
                            c.sendall(Data[-3].encode("ascii", errors='ignore'))
                if re.search("U2", Data[-4]):
                    if len(Data) != x:
                        print(Data[-4])
                        x = len(Data)
                        for c in clients:
                            c.sendall(Data[-4].encode("ascii", errors='ignore'))
        except Exception:
            for c in clients:
                c.sendall(b'Los datos [Lora] no se pueden enviar')
            
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
            threading.Thread(target=handler_message, args=(client,), daemon=True).start()
        except:
            break
            
def start_socket_server():
    global running, socket_thread
    running = True
    socket_thread = threading.Thread(target=recive_connection, daemon=True)
    lora_thread = threading.Thread(target=send_lora_msg, daemon=True)
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