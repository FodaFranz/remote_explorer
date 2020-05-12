import socket
from Crypto.Cipher import AES

password = "security"

def decrypt_string(encrypted_msg, msg_len):
    obj = AES.new(b'\x9b\x9b\x0ct\x8e\x13KQ\xcb&s\xa7\xe7\xf7R4', AES.MODE_CBC, "This is an IV456")
    plain_pw = obj.decrypt(encrypted_msg)

    return plain_pw.decode("utf-8")[:msg_len]

def check_password(pw):
    if pw == password:
        return True
    else:
        return False

PORT = 1234
HOST = socket.gethostname()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen()

connection_socket, client_address = s.accept()
print(f"{client_address} connected")

msg_len = -1

while msg_len == -1:
    confirm_message = connection_socket.recv(16)
    msg_len = connection_socket.recv(1024)
    msg_len = int(msg_len.decode("utf-8"))

client_password = decrypt_string(confirm_message, msg_len)

if check_password(client_password) == True:
    connection_socket.send(b"Success")
    while True:
        print("IN IT")
else:
    connection_socket.send(b"Failure")