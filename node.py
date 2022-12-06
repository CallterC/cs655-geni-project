'''
Author: Jinqi Lu
Prof. Matta
CS 655 PA3 GENI-MINILAB
Boston University
December 8, 2022
python node.py <port number>
This script runs on its own.
'''

### Import Libraries ###
import sys, socket, threading, concurrent.futures
from datetime import datetime
from helper import *

### Global Variables ###
script_name = "node.py"
python_head = "python"
debug = True
encoding = "utf-8"
sending_length = 1024
###payload related settings###
'''
formate of a complete payload
<start>password_md5<SEP>calc_range_start<SEP>calc_range_end(exclusive)<SEP>check_sum<end>
'''
sep = "<SEP>"
edge_start = "<start>"
edge_end = "<end>"
pw_idx = 0
range_start_idx = 1
range_end_idx = 2
chk_idx = 3

### Placeholder Variables ###
bind_address = "0.0.0.0"
bind_port = 9902

#multithreaded body
class SubThread(threading.Thread):
    def __init__(self, csocket):
        self.connection = csocket
        self.encoding = encoding
        self.debug = debug
    def run(self):
        self.start_listen(self.connection, self.encoding, self.debug)

    def check_payload_ok(self, payload_list):
        if(len(payload_list) == 4 and check_sum_ok(payload_list)):
            return True
        else:
            return False
    def start_listen(self, connection, encoding = encoding, debug = debug):
        #first receive the payload from upper level
        payload = decode_payload_into_list(receive_all(connection, 1024), edge_start, edge_end, sep)
        #check if payload invalid
        if(not self.check_payload_ok(payload)):
            #end the function immediagely
            print_with_time("Got a corrupted payload: " + payload)
            #close the connection
            connection.close()
            #end the function
            return





#initialize the global variables
def initialize():
    global bind_port, bind_address
    #Check for arguments
    if(debug):
        print_with_time("Length of arguments: " + str(len(sys.argv)))
    if(len(sys.argv) != 2):
        print_with_time("Insufficient or excess arguments! Please use " + python_head + " " + script_name + " <bind port>")
        exit(1)
    bind_port = sys.argv[1]

    #check for valid port number
    if (is_int(bind_port, True,0,65536)):
        bind_port = int(bind_port)
    else:
        print_with_time("Invalid port number! Please use INTEGER between 0 and 65535.")
        exit(1)
    if(debug):
        print_with_time("Valid port, port: " + str(bind_port))
    print_with_time("Binding to port: " + bind_port)

#create sockert listener
def run_listener():
    # create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((bind_address, bind_port))
    except:
        print_with_time("Error on binding port! Is there a server instance already running?")

    return sock

# main method
def main():
    print(decode_payload_into_list(b"<edge>password_md5<SEP>calc_range_start<SEP>calc_range_end(exclusive)<SEP>check_sum<edge>", edge_start, edge_end, sep, encoding))

    ## initialization, accept and update global variables.
    initialize()
    #send and print the message
    return




#invoke the main function
if __name__== "__main__":
    main()
