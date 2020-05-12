import socket
from Crypto.Cipher import AES

def decrypt_string(encrypted_msg, msg_len):
    obj = AES.new(b'\x9b\x9b\x0ct\x8e\x13KQ\xcb&s\xa7\xe7\xf7R4', AES.MODE_CBC, "This is an IV456")
    plain_pw = obj.decrypt(encrypted_msg)

    return plain_pw.decode("utf-8")[:msg_len]

#def check_password(pw):

PORT = 1234
HOST = socket.gethostname()

password = "security"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen()

connection_socket, client_address = s.accept()
print(f"{client_address} connected")

confirm_message = connection_socket.recv(1024)
msg_len = connection_socket.recv(1024)
msg_len = int(msg_len.decode("utf-8"))
client_password = decrypt_string(confirm_message, msg_len)
print(client_password)

# while True:
#     data = connection_socket.recv(1024)
#     data_str = data.decode("utf-8")

#     print(data_str)
    # if data != 0:
    #     if "init" in data_str:
    #         pw = decrypt_string(data_str.replace("init:",""))
    #         if data_str.replace("init:","") == password:
    #             print("Allow connection")
    #             connection_socket.send(bytes("Connection established", "utf-8"))
    #         else:
    #             print("Wrong password")
    #             connection_socket.send(bytes("Wrong password","utf-8"))
    #             connection_socket.close()
    #             break            