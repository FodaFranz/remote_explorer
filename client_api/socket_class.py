import socket
import sys
import uuid
import message
from Crypto.Cipher import AES

class Client:
    def connect(self, ip, port, password):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, port))

        #send credentials
        encrypted_pw, msg_len = self.encrypt_string(password)
        self.s.send(b"Establishing connection")
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

    #Send and wait for response
    def send(self, content):
        msg = message.Message(content)
        self.s.send(bytes(msg.get_string()))
        response = self.listen_for_response(msg)
        return response

    def listen_for_response(self, msg):
        data_str = None
        while msg.is_done == False:
            data = self.s.recv(1024)
            data_str = data.decode("utf-8")
            print(data_str)
            if(data_str.__contains__(str(msg.id))):
                msg.is_done = True
                self.msg_list.append(msg)
                
        return data_str

    def encrypt_string(self, msg):
        obj = AES.new(b'\x9b\x9b\x0ct\x8e\x13KQ\xcb&s\xa7\xe7\xf7R4', AES.MODE_CBC, "This is an IV456")
        msg_len = len(msg)
        if msg_len % 16 != 0:
            msg += ("x" * (16 - msg_len%16))

        encrypted_text = obj.encrypt(msg)
        return (encrypted_text, msg_len)

    def close(self):
        self.s.close()

    