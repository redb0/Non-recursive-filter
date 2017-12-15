
class Document:
    file_name = ""
    data = None

    def __init__(self, file):
        self.file_name = file

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def get_name(self):
        return self.file_name

    def is_opened(self):
        if self.file_name != "":
            return True
        return False
