import subprocess
import getpass
from enum import Enum

class Commands(Enum):
  next_dir = 0
  prev_dir = 1
  list_dir = 2

username = getpass.getuser()
current_path = r"/home/"+username

def exec_command(comm_num):
  comm_id = Commands(comm_num)
  if comm_id == Commands.prev_dir:
    return exec_prev_dir()

  if comm_id == Commands.list_dir:
    return exec_list_dir()

  if comm_id == Commands.next_dir:
    return exec_next_dir()


def exec_next_dir(directory_name):
  dirs = exec_list_dir()
  dir_exists = False
  for x in dirs:
    if x == directory_name:
      dir_exists = True
      break

  if dir_exists:
    current_path += directory_name
  else:
    return f"Directory {directory_name} doesn't exist"
  
  return exec_list_dir()

def exec_prev_dir():
  list_path = current_path.split("/")
  del list_path[-1]
  current_path = ""
  for x in list_path:
    current_path += "/" + x

  return exec_list_dir()


def exec_list_dir():
  result = subprocess.run(["dir", "-l"], cwd=current_path, stdout=subprocess.PIPE)
  result_list = result.stdout.decode("utf-8").split("\n")
  for x in result_list:
    print(x)

  return result_list
