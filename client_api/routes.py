from flask import Flask
from flask import request
from markupsafe import escape

from networking import socket_class
import socket_list
import command_types as ct

app = Flask(__name__)

@app.route("/connect/")
def connect():
    ip = request.args.get("ip")
    port = request.args.get("port")
    pw = request.args.get("password")
    client_id = request.args.get("client_id")

    socket = socket_class.Client()

    response = socket.connect(ip, int(port), pw)

    if response == 0:
        socket_list.new_socket(client_id, socket)
        return "Connection established"
    elif response == -1:
        return "Wrong password"
    
    return "Something went wrong connecting to the server"

@app.route("/send/")
def send():
    msg = int(request.args.get("msg"))
    comm_id = ct.Command_Types(msg)

    client_id = request.args.get("client_id")
    
    if comm_id == ct.Command_Types.next_dir:
        directory = request.args.get("directory")
        response = socket_list.get_socket(client_id).send(msg, directory)
    elif comm_id == ct.Command_Types.get_file:
        filename = request.args.get("filename")
        response = socket_list.get_socket(client_id).send(msg, filename)
    else:
        response = socket_list.get_socket(client_id).send(msg)

    return response

@app.route("/close/")
def close():
    client_id = request.args.get("client_id")
    socket_list.close_socket(client_id)
    return "Connection closed"

@app.route("/test/")
def test():
    return "Test-endpoint"
