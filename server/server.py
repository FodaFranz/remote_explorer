import socket
import sys
from Crypto.Cipher import AES

import command
import header

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

def send(content, connection_socket, msg_id):
    header_msg = header.Header(len(content), msg_id)
    connection_socket.send(bytes(header_msg.get_string(), "utf-8"))

    connection_socket.send(content)

def send_as_list(msg, connection_socket, msg_id):
    line = ""
    for x in msg:
        line += str(x).strip() + "\n"

    line_bytes = bytes(line, "utf-8")
    send(line_bytes, connection_socket, msg_id)

def open_connection(connection_socket):
    connection_socket.send(b"0")
    while True:
        data = connection_socket.recv(512)
        
        #Client disconnect
        if len(data) == 0:
            print("Client disconnect")
            listen_for_connection()

        data_str = data.decode("utf-8")
        #<command-id>:<directory/filename>:<msg-id>
        if data_str != '':
            command_id = int(data_str.split(":")[0])
            result = None
            if command_id == 0:
                #Go into directory
                directory = data_str.split(":")[1]
                msg_id = data_str.split(":")[2]
                result = command.exec_command(command_id, directory)
                send_as_list(result, connection_socket, msg_id)
            elif command_id == 3:
                #Send file
                filename = data_str.split(":")[1]
                msg_id = data_str.split(":")[2]
                result = command.exec_command(command_id, filename)
                
                send(result, connection_socket, msg_id)
            else:
                msg_id = data_str.split(":")[1]
                result = command.exec_command(int(command_id))
                send_as_list(result, connection_socket, msg_id)


def listen_for_connection():
    print(f"Listening on {HOST}:{PORT}")
    connection_socket, client_address = s.accept()
    print(f"{client_address} connected")

    confirm_message = connection_socket.recv(16)
    msg_len = connection_socket.recv(2)
    msg_len = int(msg_len.decode("utf-8"))

    client_password = decrypt_string(confirm_message, msg_len)
    if check_password(client_password) == True:
        open_connection(connection_socket)
    else:
        connection_socket.send(b"-1")

#Get host and port parameter from command line
PORT = int(sys.argv[2])
HOST = sys.argv[1]

#Create socket and start listenenig
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
#Accept only 1 concurrent connection
s.listen(1)

listen_for_connection()