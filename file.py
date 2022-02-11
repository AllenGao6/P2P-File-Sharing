'''
    objective of file.py:

    define the object class for file,   

    information to include:

    name
    size of file
    chunk list (should automaticlly be splitted into chunks, each chunk should have indicator)


    
'''
class File:

    file_name = ""
    file_size = 0
    # will be decided later how to handle indicator and hashing for each chunk, most likely will define a chunk hash function
    chunk_list = []

    def __init__(self, file_name, file_size):
        file_name = file_name
        file_size = file_size
        chunk_list = self.chunkize(file_size)

    # pre-define chunk indicator given the size of the file
    def chunkize(self):
        # will be implemented later when more research on socket programming is done 
        # given the size avaiable for the transmission

    # get the name of this file
    def getName(self):
        return self.file_name

    # get the size of this file
    def get_file_size(self):
        return self.file_size

    