import uuid
import command_types as ct

#Message format:
#<command-id>:<message:id>:[<parameter>]

class Message:
    def __init__(self, command_id=None, parameter=None):
        self.command_id = command_id
        self.is_done = False
        if command_id != None:
            self.id = uuid.uuid4()
        else:
            self.id = None
        self.parameter = parameter

    def get_command_id(self):
        return ct.Command_Types(self.command_id)

    def get_from_string(self, string):
        try:
            command_id = int(string.split(":")[0])
            msg_id = string.split(":")[1]
            if len(string.split(":")) > 2:
                parameter = string.split(":")[2]
            else:
                parameter = None
        except:
            return "Could not create message"
        
        self.command_id = command_id
        self.id = msg_id
        self.parameter = parameter

    def change_done(self):
        self.is_done = not self.is_done

    def get_string(self):
        if self.parameter != None:
            msg_string = str(self.command_id) + ":" + str(self.id) + ":" + self.parameter
        else:
            msg_string = str(self.command_id) + ":" + str(self.id)
        
        return msg_string
