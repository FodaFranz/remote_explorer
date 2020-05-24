import socket
import sys
import uuid
from . import message
from Crypto.Cipher import AES

class Client:
    def connect(self, ip, port, password):
        #List to store all completed messages (operations)
        self.msg_list = []

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((str(ip), int(port)))

        #msg_len is the length of the real message without appended 'x's
        encrypted_pw, msg_len = self.encrypt_string(password)
        self.s.send(encrypted_pw)
        msg_len = str(msg_len)
        if len(msg_len) < 2:
            msg_len = "0" + msg_len
        
        print(msg_len)
            
        self.s.send(bytes(str(msg_len), "utf-8"))

        #wait for answer
        response_bytes = self.s.recv(1024)
        response = int(response_bytes.decode("utf-8"))
        if response == 0:
            print("Connection accepted")
            return True
        elif response == -1:
            print("Connection denied")
            return False

    #Send and wait for response
    def send(self, content, directory = None):
        msg = message.Message(content, directory)
        self.s.send(bytes(msg.get_string(), "utf-8"))
        response = self.listen_for_response(msg)
        return response

    def listen_for_response(self, msg):
        data_str = None
        while msg.is_done == False:
            header = self.s.recv(64)
            header_str = header.decode("utf-8")
            msg_length = int(header_str.split(":")[0])
            msg_id = header_str.split(":")[1]
            #Receive msg-content if msg-ids allign
            if msg_id == str(msg.id):                    
                msg.change_done()
                data = self.s.recv(msg_length)
                self.msg_list.append(msg)
                if msg.content == "3":
                    return data

                data_str = data.decode("utf-8")

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

    