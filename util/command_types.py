from enum import Enum

class Command_Types(Enum):
  next_dir = 0
  prev_dir = 1
  list_dir = 2
  get_file = 3