'''
    objective of node.py:

    define the object class for node,   

    information to include:

    name
    ip address
    port to connect
    a list of file objective

'''

from file import File

class Node:

    node_name = ""
    ip_addr = ""
    port_num = 0
    file_list = []

    def __init__(self, node_name, ip_addr, port_num):
        node_name = node_name
        ip_addr = ip_addr
        port_num = port_num

    # check if the given ip address is the same as this node's ip address
    def check_ip(self, input_ip):
        return self.ip_addr == input_ip

    # get the name of the peer node
    def getName(self):
        return self.node_name
    
    # get the ip address of this peer node
    def get_ip_addr(self):
        return self.ip_addr

    # get the port number of this peer node
    def get_port(self):
        return self.port_num

    # get the file list of this peer node
    def get_file_list(self):
        return self.file_list

    # register a new file on this node
    def register_file(self, file_name, file_size):
        new_file = File(file_name, file_size)
        file_list.append(new_file)

    # check if a particular file exist in this node
    def check_file_exit(self, name):
        for file in self.file_list:
            if file.getName() == name:
                return True
        return False

    # get a particular file object given name
    def get_file(self, name):
        for file in self.file_list:
            if file.getName() == name:
                return file
        return None
        
    
