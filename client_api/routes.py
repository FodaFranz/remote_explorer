from flask import Flask
from flask import request
from markupsafe import escape

import socket_class

app = Flask(__name__)

socket = socket_class.Client()

@app.route("/connect/")
def connect():
    ip = request.args.get("ip")
    port = request.args.get("port")

    socket.connect(ip, int(port), "security")
    return "Connect page"

@app.route("/send/")
def send():
    msg = request.args.get("msg")
    socket.send(msg)
    return "Sent"

@app.route("/close/")
def close():
    socket.close()
    return "Connection closed"