from flask import Flask, render_template, redirect, url_for, request, jsonify
import socket_server
import random
import subprocess
import time
cmd = "python C:/Users/zil08/OneDrive/Documents/Cansat-APP/ilernsat/main_lora.py"
data = []
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crear_conexion', methods=['POST'])
def crear_conexion():
    socket_server.start_socket_server()
    return redirect(url_for('conection'))

@app.route('/conection')
def conection():
    return render_template('conection.html', ip=socket_server.IP, port=socket_server.PORT)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', msg='')

@app.route("/data")
def get_data():
    timestamp = time.time()
    value = random.randint(10, 100)
    data.append([timestamp, value])
    if len(data) > 10:
        data.pop(0)
    return jsonify(data)

@app.route('/go_dashboard')
def go_dashboard():
    return redirect(url_for('dashboard'))
    
@app.route('/close_conection')
def close_conection():
    socket_server.stop_socket_server()
    return redirect(url_for('index'))

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form.get('message', '')
    if message:
        socket_server.send_message(message)
    return render_template('dashboard.html', msg=message)

import atexit
atexit.register(socket_server.stop_socket_server)
# op = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

if __name__ == '__main__':
    app.run(debug=True)