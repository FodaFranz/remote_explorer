from flask import Flask
from flask import request
from markupsafe import escape

from networking import socket_class
import socket_list

app = Flask(__name__)

#socket = None

#TODO:
# Give url unique id and store those unique ids with the sockets in redis 
# or something similiar

@app.route("/connect/")
def connect():
    ip = request.args.get("ip")
    port = request.args.get("port")
    pw = request.args.get("password")
    client_id = request.args.get("client_id")

    socket = socket_class.Client()

    isConnectSuccessfull = socket.connect(ip, int(port), pw)

    if isConnectSuccessfull:
        socket_list.new_socket(client_id, socket)
        return "Connection successfull"
    else:
        return "Connection unsuccessfull"

@app.route("/send/")
def send():
    msg = request.args.get("msg")
    client_id = request.args.get("client_id")
    if int(msg) == 0:
        directory = request.args.get("directory")    
        response = socket_list.get_socket(client_id).send(msg, directory)
    else:
        response = socket_list.get_socket(client_id).send(msg)
    return response

@app.route("/close/")
def close():
    client_id = request.args.get("client_id")
    
    socket_list.close_socket(client_id)
    return "Connection closed"