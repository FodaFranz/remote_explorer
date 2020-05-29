import json
from json import JSONEncoder

class Explorer_Object:
    is_file = None
    size = None
    creation_time = None
    name = None
    
    def __init__(self, string):
        super().__init__()

        string_split = string.split(" ")
        #Remove empty strings from array
        string_split = list(filter(None, string_split))
        if len(string_split) > 0:
            self.is_file = True if string_split[0][0] == "d" else False
            self.size = int(string_split[4])
            self.creation_time = string_split[5] + " " + string_split[6] + " " + string_split[7]
            self.name = string_split[8]
    
    def get_string(self):
        return "File" if self.is_file else "Directory" + self.name + " " + self.creation_time + " " + self.size

class Explorer_Object_Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__