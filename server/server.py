import socket
import sys
from Crypto.Cipher import AES

import command

password = "security"
delimiter = '$'

def decrypt_string(encrypted_msg, msg_len):
    obj = AES.new(b'\x9b\x9b\x0ct\x8e\x13KQ\xcb&s\xa7\xe7\xf7R4',
                  AES.MODE_CBC, "This is an IV456")
    plain_pw = obj.decrypt(encrypted_msg)
    return plain_pw.decode("utf-8")[:msg_len]


def check_password(pw):
    if pw == password:
        return True
    else:
        return False


def send_list_to_client(msg, connection_socket, msg_id):
    line = ""
    for x in msg:
        line += str(x).strip() + " "

    line += delimiter + msg_id

    line_bytes = bytes(line, "utf-8")
    connection_socket.send(line_bytes)

def open_connection(connection_socket):
    connection_socket.send(b"Success")
    while True:
        data = connection_socket.recv(512)
        
        #Client disconnect
        if len(data) == 0:
            print("Client disconnect")
            listen_for_connection()

        data_str = data.decode("utf-8")
        if data_str != '':
            print(data_str)
            if data_str == "Establishing connection":
                print("This server is already in use")
            else:
                try:
                    command_id = data_str.split(":")[0]
                    msg_id = data_str.split(":")[1]
                    result = command.exec_command(int(command_id))
                    send_list_to_client(result, connection_socket, msg_id)
                except:
                    connection_socket.send(b"Received invalid data")
                    print("Received invalid data")

def listen_for_connection():
    print(f"Listening on {HOST}:{PORT}")
    connection_socket, client_address = s.accept()
    print(f"{client_address} connected")

    f_data = connection_socket.recv(23)
    f_data_str = f_data.decode("utf-8")
    confirm_message = b""
    msg_len = b""

    if f_data_str == "Establishing connection":
        confirm_message = connection_socket.recv(16)
        msg_len = connection_socket.recv(1024)
        msg_len = int(msg_len.decode("utf-8"))

    client_password = decrypt_string(confirm_message, msg_len)
    if check_password(client_password) == True:
        open_connection(connection_socket)
    else:
        connection_socket.send(b"Failure")

PORT = int(sys.argv[2])
HOST = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)

listen_for_connection()