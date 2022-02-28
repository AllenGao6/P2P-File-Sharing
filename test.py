# import base64

# path = "test.png"
# #path = "test.pdf"

# with open(path, "rb") as any_file:
#     encoded_string = any_file.read()

# #print(encoded_string)

# g = open("out.png", "w")
# g.write(encoded_string.decode("utf-8") )
# g.close()

import base64
import sys
import hashlib
  
  
with open("test.png", "rb") as image2string:
    converted_string = base64.b64encode(image2string.read())
print(converted_string)
  
def hash_chunk(data):
    # implement sha1 for verification
    # create sha3-256 hash objects
    obj_sha3_256 = hashlib.sha3_256(data)
 
    # print in hexadecimal
    print("\nSHA3-256 Hash: ", obj_sha3_256.hexdigest())
    return  obj_sha3_256.hexdigest()
  
# decodeit = open('hello_level.png', 'wb')
# decodeit.write(base64.b64decode((converted_string)))
# decodeit.close()

a = hash_chunk(converted_string)
