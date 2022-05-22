'''
TCP Client file to transmit data to receiver.
'''

import time
import data_to_send
import socket
import json
import sys

#if len(sys.argv) > 1:
#    HOST = sys.argv[1]  # Standard loopback interface address (localhost)
#    PORT = sys.argv[2]  # Port to listen on (non-privileged ports are > 1023)
#else:
#    HOST = None
#    PORT = None

#if HOST is None:
#    HOST = "localhost"  # The server's hostname or IP address
#if PORT is None:
#    PORT = 65432  # The port used by the server

packet = data_to_send.captureData() # dictionary
data_string = json.dumps(packet) #data serialized (dict -> str obj)
data_dict = str.encode(data_string) # converts serialized data to bytes from str obj

# also write json to file to access, keep appending data to data_all, replace for data
try:
    f_all = open("/home/pi/ece5725/receiver/data_all.json", "a")
    f_all.write(data_string)
    f_all.close()
    f = open("/home/pi/ece5725/receiver/data.json", "w")
    f.write(data_string)
    f.close()
except:
    print("not saved, error occured")
    print("Error: "+sys.exc_info())
    sys.exit(2)

#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#    s.connect((HOST, PORT))
#    s.sendall(data_dict)
