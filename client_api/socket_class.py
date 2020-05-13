import socket
import sys
from Crypto.Cipher import AES

class Client:
    def connect(self, ip, port, password):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, port))

        #send credentials
        encrypted_pw, msg_len = self.encrypt_string(password)
        self.s.send(encrypted_pw)
        msg_len_str = str(msg_len)
        self.s.send(bytes(msg_len_str))

        #wait for answer
        response = self.s.recv(1024)
        response_str = response.decode("utf-8")
        if response_str == "Success":
            print("Connection accepted")
        else:
            print("Connection denied")

    def send(self, msg):
        self.s.send(bytes(msg, "utf-8"))

    def encrypt_string(self, msg):
        obj = AES.new(b'\x9b\x9b\x0ct\x8e\x13KQ\xcb&s\xa7\xe7\xf7R4', AES.MODE_CBC, "This is an IV456")
        msg_len = len(msg)
        if msg_len % 16 != 0:
            msg += ("x" * (16 - msg_len%16))

        encrypted_text = obj.encrypt(msg)
        return (encrypted_text, msg_len)


    