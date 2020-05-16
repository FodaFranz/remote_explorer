from flask import Flask
from flask import request
from markupsafe import escape

import socket_class

app = Flask(__name__)

socket = None

#TODO:
# Give url unique id and store those unique ids with the sockets in redis 
# or something similiar

@app.route("/connect/")
def connect():
    ip = request.args.get("ip")
    port = request.args.get("port")
    pw = request.args.get("password")

    socket = socket_class.Client()

    socket.connect(ip, int(port), pw)
    return "Connect page"

@app.route("/send/")
def send():
    msg = request.args.get("msg")
    response = socket.send(msg)
    return response

@app.route("/close/")
def close():
    socket.close()
    return "Connection closed"