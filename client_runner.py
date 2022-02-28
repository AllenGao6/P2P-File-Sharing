import argparse
from functools import total_ordering
import os.path
from os import path
import os
from file import File
from client import *

parser = argparse.ArgumentParser(description='Choose an action to perform in this P2P network')

# select action
parser.add_argument('--reg', default=False, action='store_true')
parser.add_argument('--file_list_request', default=False, action='store_true')
parser.add_argument('--download', default=False, action='store_true')

args = parser.parse_args()
#

# select action
reg= args.reg
file_list_request = args.file_list_request
download = args.download

total_ordering = reg + file_list_request + download

if total_ordering == 0:
    print("Please Select an Action")
    exit()
elif total_ordering > 1:
    print("Please Select One Action At a Time")
    exit()

if reg: 
    # Register Request: Tells the server what files the peer
    # wants to share with the network. Takes in the IP address
    # and port for the endpoint to accept peer connections for
    # download; the number of files to register; and for every
    # file, a file name and its length.
    # check for error
    file_entry = []
    # enter port number to verify the client information
    port = input("Please enter your port number for incoming connection: ")
    if not port.isnumeric():
        print("Please Enter a Valid Port Number")
        exit()

    # let user enter all file they wish to upload
    file_input = input("Please enter all file path you wish to register: (Seperate by a single space)")
    if len(file_input) != 0:
        file_list = file_input.split(" ")
        for file in file_list:
            if not path.exists(file):
                print(file + " NOT FOUND")
                exit()
        file_entry += file_list

    # let user to enter a dir to upload
    dir_input = input("Please enter the dirctory you want to upload: (Seperate by a single space)")
    if not path.isdir(dir_input):
        print(dir_input + " NOT FOUND")
        exit()
    for file in os.listdir(dir_input):
        file_entry.append(os.path.join(dir_input, file))

    # register the file in client side 
    added_file = register_local_file(file_entry)

    send_package = []
    for file in added_file:
        send_package.append((file.getName(), file.get_file_size()))

    # sending the package
    result = send_server_request(100, send_package, port)
    if not result:
        remove_files(added_file, "obj")
        print("registered failed, please try again")
    else:
        remove_file = []
        for filename, status in result.items():
            if status == "Failed":
                remove_file.append(filename)
        remove_files(remove_file, "name")

        if len(remove_file) == 0:
            print("All file registered successfully")
        else:
            file_str = ", ".join(remove_file)
            print("File failed to register: " + file_str)
    
elif file_list_request:
    # File List Request: Asks the server for the list of files. 
    result = send_server_request(200)
    if not result:
        print("Failed to get file list")
    else:
        for filename, size in result.items():
            print(filename + " : " + str(size))

elif download:
    filename = input("Enter the file you wish to download: (Select extractly like file list): ")
    
else:
    # File Chunk Request: Asks the peer to return the file
    # chunk. Reads in a file name, chunk indicator.
    pass


