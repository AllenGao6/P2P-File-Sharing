
class File_record:
    file_name = ""
    file_size = 0
    chunk_list = []
    CHUNK_SIZE = 2048

    def __init__(self, file_name, file_size):
        self.file_name = file_name
        self.file_size = file_size
        self.chunk_list = [True] * (self.file_size // self.CHUNK_SIZE + 1)

    def get_filename(self):
        return self.file_name

    def get_file_size(self):
        return self.file_size

    def get_chunk_list(self):
        return self.chunk_list

    def get_index_chunk(self, index):
        if index >= len(self.chunk_list):
            return None
        return self.chunk_list[index]
    