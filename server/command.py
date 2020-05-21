import subprocess
import getpass
from enum import Enum

class Commands(Enum):
  next_dir = 0
  prev_dir = 1
  list_dir = 2

username = getpass.getuser()
current_path = r"/home/"+username

def exec_command(comm_num, directory=None):
  comm_id = Commands(comm_num)
  if comm_id == Commands.prev_dir:
    return exec_prev_dir()

  if comm_id == Commands.list_dir:
    return exec_list_dir()

  if comm_id == Commands.next_dir:
    return exec_next_dir(directory)

def exec_next_dir(directory_name):
  global current_path
  current_path += "/" + directory_name
  return exec_list_dir()

def exec_prev_dir():
  global current_path
  if current_path != "/home":  
    list_path = current_path.split("/")
    del list_path[-1]
    current_path = ""
    for x in list_path:
      if x != "":
        current_path += "/" + x
  
  return exec_list_dir()

def exec_list_dir():
  global current_path
  result = subprocess.run(["dir", "-l"], cwd=current_path, stdout=subprocess.PIPE)
  result_list = result.stdout.decode("utf-8").split("\n")

  return result_list
