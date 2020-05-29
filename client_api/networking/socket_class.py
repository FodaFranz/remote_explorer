import socket
import sys
import uuid
import message
import command_types as ct
import explorer_object as eo
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
        #msg_len gets recv'd at an constant size so we add 0s to fill that space
        if len(msg_len) < 2:
            msg_len = "0" + msg_len
        self.s.send(bytes(msg_len, "utf-8"))

        #wait for answer 
        #0 -> connection successfull
        #-1 -> wrong password
        response = self.s.recv(2)
        return int(response.decode("utf-8"))

    #Send and wait for response
    #parameter is the directory to go into or the file to request
    def send(self, content, parameter = None):
        #Msg-format
        #<command-id>:<message:id>:[<parameter>]
        msg = message.Message(content, parameter)
        self.s.send(bytes(msg.get_string(), "utf-8"))
        response = self.listen_for_response(msg)

        return response

    def listen_for_response(self, msg):
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
                if msg.get_command_id == ct.Command_Types.get_file:
                    return data

                data_str = data.decode("utf-8")
                #Parse data_str in list of explorer_objects
                explorer_objects = []
                for x in data_str.split("\n")[1:]:
                    explorer_objects.append(eo.Explorer_Object(x))

                return explorer_objects

        return "Something went wrong"

    def encrypt_string(self, msg):
        obj = AES.new(b'\x9b\x9b\x0ct\x8e\x13KQ\xcb&s\xa7\xe7\xf7R4', AES.MODE_CBC, "This is an IV456")
        msg_len = len(msg)
        if msg_len % 16 != 0:
            msg += ("x" * (16 - msg_len%16))

        encrypted_text = obj.encrypt(msg)
        return (encrypted_text, msg_len)

    def close(self):
        self.s.close()

    