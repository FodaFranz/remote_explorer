import subprocess
from enum import Enum

class Commands(Enum):
  next_dir = 0
  prev_dir = 1
  list_dir = 2

current_path = "~"

def exec_command(comm_num):
  try:
    if comm_num == Commands.prev_dir:
      return exec_prev_dir()

    if comm_num == Commands.list_dir:
      return exec_list_dir()
  except:
    return "Error"


def exec_prev_dir():
  list_path = current_path.split("/")
  del list_path[-1]
  current_path = ""
  for x in list_path:
    current_path += x + "/"
  
  print(current_path)
  return exec_list_dir()

def exec_list_dir():
  result = subprocess.run("dir", stdout=subprocess.PIPE)
  result_list = result.stdout.decode("utf-8").split(" ")
  filtered_result_list = list(filter(None, result_list))
  return filtered_result_list
