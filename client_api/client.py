import socket
import sys
from Crypto.Cipher import AES

def encrypt_string(msg):
    obj = AES.new(b'\x9b\x9b\x0ct\x8e\x13KQ\xcb&s\xa7\xe7\xf7R4', AES.MODE_CBC, "This is an IV456")
    msg_len = len(msg)
    if msg_len % 16 != 0:
        msg += ("x" * (16 - msg_len%16))

    encrypted_text = obj.encrypt(msg)

    return (encrypted_text, msg_len)

PORT = 1234
HOST = socket.gethostname() 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print(f"Connected to {HOST}")

encrypted_pw, msg_len = encrypt_string("security")
s.send(encrypted_pw)
s.send(bytes(str(msg_len), "utf-8"))

data = s.recv(1024)
data_str = data.decode("utf-8")
if data_str == "Success":
    print("Connection established")
    while True:
        command = input("Command: ")
        if command == "send":
            s.send(b"2")
        
        data = s.recv(1024)
        print(data.decode("utf-8"))

elif data_str == "Failure":
    print("Connection refused")