import uuid
import dal

class Socket:
    def __init__(self, client_id, socket_id, s):
        self.client_id = client_id
        self.socket_id = socket_id
        self.s = s
    
    def get_string(self):
        return str(self.client_id) + ":" + str(self.socket_id)

sockets = []

def new_socket(client_id, s):
    socket = Socket(client_id, uuid.uuid4(), s)
    #Check if client already has an open socket
    if get_socket(client_id) != None:
        return -1

    sockets.append(socket)
    dal.add_socket(client_id, str(socket.socket_id))
    return 0

def get_socket(client_id):
    for x in sockets:
        if x.client_id == client_id:
            return x.s

    return None

def close_socket(client_id):
    get_socket(client_id).close()
    dal.remove_socket(client_id)
