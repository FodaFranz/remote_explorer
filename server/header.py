class Header:
    def __init__(self, msg_length, msg_id):
        super().__init__()
        self.msg_length = msg_length
        self.msg_id = str(msg_id)
        self.length = 64
    
    def get_string(self):
        remaining_space = self.length - (len(self.msg_id) + 1) - len(str(self.msg_length))
        msg_length_str = ("0" * remaining_space) + str(self.msg_length)
        return msg_length_str + ":" + self.msg_id