import uuid

class Message:
    def __init__(self, content, directory=None):
        self.content = content
        self.is_done = False
        self.id = uuid.uuid4()
        self.directory = directory

    def change_done(self):
        self.is_done = not self.is_done

    def get_string(self):
        if self.directory != None:
            msg_string = self.content + ":" + self.directory + ":" + str(self.id)
            return msg_string
        else:
            msg_string = self.content + ":" + str(self.id)
            return msg_string
