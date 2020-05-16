import uuid

class Message:
    def __init__(self, content):
        self.content = content
        self.is_done = False
        self.id = uuid.uuid4()

    def change_done(self):
        self.is_done = not self.is_done

    def get_string(self):
        msg_string = self.content + ":" + str(self.id)
        return msg_string
