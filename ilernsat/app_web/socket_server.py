import socket
import threading
import time

clients = []
listener = None
socket_thread = None
running = False

IP = socket.gethostbyname(socket.gethostname())
PORT = 4444

def handler_message(client):
    while running:
        try:
            msg = client.recv(1024)
            if not msg:
                break
            SMS = f"{msg.decode('ascii', errors='ignore')} => {time.ctime(time.time())}"
            with open("data.txt", "a") as f:
                f.write(SMS + "\n")
            print(SMS)
        except:
            break
    client.close()
    if client in clients:
        clients.remove(client)

def send_message(msg):
    SMS = f"{msg} => {time.ctime(time.time())}"
    with open("data.txt", "a") as f:
        f.write(SMS + "\n")
    for c in clients:
        c.sendall(msg.encode("ascii", errors='ignore'))

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
    socket_thread.start()

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
