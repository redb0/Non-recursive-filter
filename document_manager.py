from document import Document


class Manager:
    list_of_files = []
    current = None

    def __init__(self):
        self.list_of_files = []
        self.current = None

    # принимает аргумент типа Document
    def add(self, file_name):
        #if self.file_ready_opened(file_name):
        new_doc = Document(file_name)
        self.list_of_files.append(new_doc)
        self.current = len(self.list_of_files) - 1

    def file_ready_opened(self, file_name):
        ready = False
        for available_file in self.list_of_files:
            if available_file.get_name() != file_name:
                ready = True
            else:
                ready = False
        return ready

    # установить текущий документ
    #def set_current(self, file_name):
    #    if self.file_ready_opened(file_name):
    #        self.current = len(self.list_of_files) - 1

    # получить имя текущего документа
    def get_current(self):
        if self.current or self.current == 0:
            return self.list_of_files[self.current].get_name()
        else:
            return None

    def clear(self):
        self.list_of_files = []
        self.current = None


global manager
manager = Manager()
