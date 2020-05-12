import subprocess
from enum import Enum

class Commands(Enum):
  next_dir = 0
  prev_dir = 1
  list_dir = 2

def exec_command(comm_num):
  try:
    if comm_num == 2:
      return exec_list_dir()
  except:
    return "Error"

def exec_list_dir():
  result = subprocess.run("dir", stdout=subprocess.PIPE)
  result_list = result.stdout.decode("utf-8").split(" ")
  filtered_result_list = list(filter(None, result_list))
  return filtered_result_list