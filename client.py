#!/usr/bin/env python3

from ipaddress import ip_address
import os
from _thread import *
import socket
import base64
import time
from file import File
import json
import hashlib




# # ip, port global info
# # host = socket.gethostbyname(socket.gethostname())
# host = '127.0.0.1'
# port = 65483

# creating local file list
local_files = []


#-----------------supporting function call-------------------
# get the file objext by file name
def get_file(name):
    for file in local_files:
        if file.getName() == name:
            return file
    return None
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

# get certain chunk data from a file
def get_file_chunk(filename, chunk_index):
    file = get_file(filename)
    if not file:
        print("Failed to find file")
        return None, None
    byte_data = file.get_index_chunk(chunk_index)
    if not byte_data:
        print("Failed to get Chunk")
        return None, None
    hashed_block = file.get_index_chunk_hash(chunk_index)
    return byte_data, hashed_block

# look for peer_addr and port for a particular index
def get_peer_info_by_index(data, index, file_name):
    for key, value in data.items():
        port, index_list = value
        if index in index_list:
            return (key, port, index, file_name)

        
# verify hash
def check_hash(byte_block, hash_block):
    # implement sha1 for verification
    obj_sha3_256 = hashlib.sha3_256(byte_block)

    if obj_sha3_256 == hash_block:
        return True
    return False



# --------------------------------Socket Content Below------------------------------#


'''
Request code:

100: register for files
200: File List Request
300: File Locations Request
400: Chunk Register Request
500: File Chunk Request
'''
# socket constant
server_host = '104.38.105.225'
# server_host = '127.0.0.1'
server_port = 65401

# this function should be placed somewhere else, put here as a shortcut
def find_local_ip_addr():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_addr = s.getsockname()[0]
    s.close()
    return local_addr

client_server_addr = find_local_ip_addr()
client_server_port = 61001

def get_client_server_addr():
    return client_server_addr

def get_client_server_port():
    return client_server_port

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
        addr_info, port_info = port
        m = {"code": request_code, "port": int(port_info), "data": data, 'addr': addr_info}
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
        res = ClientSocket.recv(8192)
        # print(res)
        # close the connection
        ClientSocket.close()
        res = json.loads(res.decode("utf-8"))
        if res['status'] == "Success":
            return res["data"]
        else:
            print(res["error"])
            return None

    elif request_code == 400: # register a chunk

        added_data = data
        added_data['peer_addr'] = get_client_server_addr()
        added_data['peer_port'] = get_client_server_port()
        m = {"code": request_code, "data": added_data}
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

def send_peer_request(peer_host, peer_port, chunk_index, file_name):

    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print('Waiting for connection')
    try:
        ClientSocket.connect((peer_host, peer_port))
    except socket.error as e:
        print(str(e))
    Response = ClientSocket.recv(2048)
    # handshake, will have other error code here, may not be necessary for this project :)
    if not check_response(Response):
        ClientSocket.close()
        return None
    # sending out request
    data = {}
    data['filename'] = file_name
    data['chunk_index'] = chunk_index
    data = json.dumps(data)
    ClientSocket.send(bytes(data,encoding="utf-8"))

    # recieve responce data
    byte_block = ClientSocket.recv(8192)
    if len(byte_block) == 0: # if the responce is 
        print("Failed to get data")
        ClientSocket.close()
        return None
    # send success response to get hash data
    data = {'status':"Success"}
    data = json.dumps(data)
    ClientSocket.send(bytes(data,encoding="utf-8"))
    # recieve hashed data
    res = ClientSocket.recv(2048)
    res = json.loads(res.decode("utf-8"))
    hash_byte = res['data']
    # check hash for data integrity
    if not check_hash(byte_block, hash_byte):
        print("Hash Does Not Match With Data")
        ClientSocket.close()
        return None
    # print out log here
    print("get file", file_name, " chunk index ", chunk_index, " from peer ", peer_host)
    
    return [byte_block, hash_byte, chunk_index]
    

# find "num" number of rarest chunk index in the whole network
# return each of their chunk_index, peer_addr, peer_port
def find_rarest_block(file, num):
    # get what we still miss
    # get what is availble on the network
    # get what we miss is most rare in the network
    # rank these rarest chunk and select top num of chunk to return
    file_name = file.getName()
    missing_local = file.get_chunk_info(find_miss=True)
    result = send_server_request(300, data=file.getName())
    chunk_frequency = {}
    for key, value in result.items():
        port, index_list= value
        for index in index_list:
            if index not in chunk_frequency:
                chunk_frequency[index] = 1
            else:
                chunk_frequency[index] += 1
    # only looking for the missing part
    for index in chunk_frequency.keys():
        if index not in missing_local:
            del chunk_frequency[index]

    # rank the frequency
    info_data = []
    sort_orders = sorted(chunk_frequency.items(), key=lambda x: x[1])
    for i in range(num):
        index, _ = sort_orders[i]
        info_data.append(get_peer_info_by_index(result, index, file_name))
    
    return info_data


