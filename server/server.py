import socket
import sys
from Crypto.Cipher import AES

import command
import header
import command_types as ct
import message

password = "security"
delimiter = '$'

def decrypt_string(encrypted_msg, msg_len):
    obj = AES.new(b'\x9b\x9b\x0ct\x8e\x13KQ\xcb&s\xa7\xe7\xf7R4',
                  AES.MODE_CBC, "This is an IV456")
    plain_pw = obj.decrypt(encrypted_msg)
    return plain_pw.decode("utf-8")[:msg_len]

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
    while True:
        data = connection_socket.recv(512)
        
        #Client disconnect
        if len(data) == 0:
            print("Client disconnect")
            listen_for_connection()

        #<command-id>:<message:id>:[<parameter>]
        data_str = data.decode("utf-8")
        msg = message.Message()
        msg.get_from_string(data_str)

        result = command.exec_command(msg)
        if msg.get_command_id() == ct.Command_Types.get_file:
            send(result, connection_socket, msg.id)
        else:
            send_as_list(result, connection_socket, msg.id)


def listen_for_connection():
    print(f"Listening on {HOST}:{PORT}")
    connection_socket, client_address = s.accept()
    print(f"{client_address} requested connection")

    confirm_message = connection_socket.recv(16)
    msg_len = connection_socket.recv(2)
    msg_len = int(msg_len.decode("utf-8"))

    client_password = decrypt_string(confirm_message, msg_len)
    if client_password == password:
        print("Connection successfull")
        connection_socket.send(b"00")
        open_connection(connection_socket)
    else:
        connection_socket.send(b"-1")

#Get host and port parameter from command line
PORT = int(sys.argv[2])
HOST = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1) #Accept only 1 concurrent connection

listen_for_connection()