'''
    will be run by each peer to get information from server, upload from server and so on
'''
#!/usr/bin/env python3

import socket
import base64
import time
import argparse
from file import File
import json



# creating local file list
local_files = []


#-----------------supporting function call-------------------
# get all filename existed locallly
def get_all_filename():
    return [file.getName() for file in local_files]

# remove a file by its name
def remove_file_by_name(name):
    for file in local_files:
        if file.getName() == name:
            local_files.remove(file)
            break

# register file to client
def register_local_file(file_list):
    added_file = []
    filename_space = get_all_filename()
    for file in file_list:
        if file not in filename_space:
            new_file = File(file)
            local_files.append(new_file)
            added_file.append(new_file)
    return added_file

#remove files from local file list
def remove_files(files, type):
    if type == "obj":
        for file in files:
            local_files.remove(file)
    if type == "name":
        for file in files:
            remove_file_by_name(file)



'''
Request code:

100: register for files
200: File List Request
300: File Locations Request
400: Chunk Register Request
500: File Chunk Request
'''
# socket constant
# server_host = '104.38.105.225'
server_host = '127.0.0.1'
server_port = 65484
def check_response(responce):
    if responce.decode('utf-8') != "200":
        print("connection failed!")
        return False
    return True

def send_server_request(request_code, data=None, port=None):
    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print('Waiting for connection')
    try:
        ClientSocket.connect((server_host, server_port))
    except socket.error as e:
        print(str(e))
    Response = ClientSocket.recv(2048)
    # handshake, will have other error code here, may not be necessary for this project :)
    if not check_response(Response):
        ClientSocket.close()
        return

    if request_code == 100: # request to register file list
        # sending code for particular request
        m = {"code": request_code, "port": int(port), "data": data}
        data = json.dumps(m)
        ClientSocket.send(bytes(data,encoding="utf-8"))

        # wait for responce
        time.sleep(0.5)
        res = ClientSocket.recv(2048)
        # close the connection
        ClientSocket.close()
        res = json.loads(res.decode("utf-8"))
        if res['status'] == "Success":
            return res["data"]
        else:
            print(res["error"])
            return None

    elif request_code == 200:
        m = {"code": request_code}
        data = json.dumps(m)
        ClientSocket.send(bytes(data,encoding="utf-8"))
        
        # waiting for the response
        res = ClientSocket.recv(2048)
        # close the connection
        ClientSocket.close()
        res = json.loads(res.decode("utf-8"))
        if res['status'] == "Success":
            return res["data"]
        else:
            print(res["error"])
            return None

    elif request_code == 300: # request file location
        m = {"code": request_code, "data": data}
        data = json.dumps(m)
        ClientSocket.send(bytes(data,encoding="utf-8"))
        
        # waiting for the response
        res = ClientSocket.recv(4096)
        # close the connection
        ClientSocket.close()
        res = json.loads(res.decode("utf-8"))
        if res['status'] == "Success":
            return res["data"]
        else:
            print(res["error"])
            return None

    elif request_code == 400: # register a chunk

        m = {"code": request_code, "data": data}
        data = json.dumps(m)
        ClientSocket.send(bytes(data,encoding="utf-8"))
        
        # waiting for the response
        res = ClientSocket.recv(2048)
        # close the connection
        ClientSocket.close()
        res = json.loads(res.decode("utf-8"))
        if res['status'] == "Success":
            return True
        else:
            print(res["error"])
            return False
        
    
    return None

        
        
        


    # Response = ClientSocket.recv(2048)
    # print(Response.decode('utf-8'))

    # m = {"id": 2, "name": "abc"} # a real dict.


    # data = json.dumps(m)

    # index = 0
    # print(len( bytelist))
    # while index != len(bytelist):
    #     # client_input = str(input("Say Something: "))
    #     # ClientSocket.send(str.encode(client_input))
    #     # time.sleep(0.2)
    #     ClientSocket.send(bytelist[index])
    #     Response = ClientSocket.recv(1024)
    #     if Response.decode('utf-8') != "200":
    #         print("process error!")
    #         break
    #     print("going througg iteration", str(index))
    #     index += 1

    # ClientSocket.close()


