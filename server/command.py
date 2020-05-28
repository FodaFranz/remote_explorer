import subprocess
import getpass
import os
import sys
import command_types as ct
import message

username = getpass.getuser()
current_path = r"/home/"+username

def exec_command(msg):
  if msg.get_command_id() == ct.Command_Types.prev_dir:
    return exec_prev_dir()

  if msg.get_command_id() == ct.Command_Types.list_dir:
    return exec_list_dir()

  if msg.get_command_id() == ct.Command_Types.next_dir:
    return exec_next_dir(msg.parameter)

  if msg.get_command_id() == ct.Command_Types.get_file:
      return get_file_as_bytes(msg.parameter)

def get_file_as_bytes(filename):
  global current_path
  file_size = os.path.getsize(current_path + "/" + filename)
  with open(current_path + "/" + filename, "rb") as f: 
    file_bytes = f.read()
    return file_bytes

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
