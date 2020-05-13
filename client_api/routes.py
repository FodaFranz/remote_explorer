from flask import Flask
from markupsafe import escape

import socket_class

app = Flask(__name__)

socket = socket_class.Client()

@app.route("/connect/<ip>")
def connect(ip):
    socket.connect("matthia", 1234, "security")
    return "IP: %s" % escape(ip)