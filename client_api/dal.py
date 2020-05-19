import redis
import uuid
import configparser

config = configparser.ConfigParser()
config.read("./config/db.ini")

host = config["CONNECTION"]["host"]
port = config["CONNECTION"]["port"]
password = config["CONNECTION"]["password"]

r = redis.Redis(host=host, port=port, db=0, password=password)

def add_socket(client_id, socket_id):
    r.set(client_id, socket_id)

def get_socket(client_id):
    return r.get(client_id)

def remove_socket(client_id):
    r.delete(client_id)