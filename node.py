'''
Author: Jinqi Lu, Quansen Wang
Prof. Matta
CS 655 PA3 GENI-MINILAB
Boston University
December 8, 2022
python node.py <port number>
This script requires the presence of helper.py to run.
'''

### Import Libraries ###
import sys, socket, threading, concurrent.futures
from datetime import datetime
from helper import *

### Global Variables ###
script_name = "node.py"
python_head = "python"
debug = False
sending_length = 1024
###payload related settings###
'''
formate of a complete payload
<start>password_md5<SEP>calc_range_start<SEP>calc_range_end(exclusive)<SEP>check_sum<end>
'''

pw_idx = 0
range_start_idx = 1
range_end_idx = 2
chk_idx = 3

### Placeholder Variables ###
#port will be override by the commandline argument
bind_address = "0.0.0.0"
bind_port = 9902

#multithreaded body
class SubThread(threading.Thread):
    def __init__(self, csocket):
        threading.Thread.__init__(self)
        self.connection = csocket
        self.encoding = encoding
        self.debug = debug
    def run(self):
        self.listen_wrapper(self.connection, self.encoding, self.debug)

    def check_payload_ok(self, payload_list):
        if(payload_list == -1):
            print_with_time("Incorrect payload!")
            return False
        elif(len(payload_list) != 4):
            print_with_time("Incorrect payload list length!")
            return False
        elif(not check_sum_ok(payload_list)):
            print_with_time("Incorrect payload checksum!")
            return False
        else:
            return True

    def crack_pw(self, hash, start, end):
        #return a list of index of inputed start
        #invalid length
        if(len(start) > 5 or len(end) > 5):
            return -1

        start_idx = get_idx_list_pw(start)
        end_idx = get_idx_list_pw(end)
        if(not checking_pw_range(start_idx,end_idx)):
            return -1

        #start to loop the hash, only ends when start and end are match and there is no interrupts(password found)
        while(not compare_two_idx_list(start_idx,end_idx)):
            #current hash
            tmd5 = get_md5_from_list(start_idx)
            if(tmd5 == hash):
                return get_str_from_list(start_idx)
            else:
                #update the index
                start_idx = update_index_list(start_idx)
                #print(get_str_from_list(start_idx))
        #test the end index
        tmd5 = get_md5_from_list(end_idx)
        if(tmd5 == hash):
            return get_str_from_list(end_idx)
        #no pw found
        return -1
    def start_listen(self, connection, encoding = encoding, debug = debug):
        #first receive the payload from upper level
        payload = decode_payload_into_list(receive_all(connection, 1024), edge_start, edge_end, sep)
        if(debug):
            print("Payload received: ")
            print(payload)
        #check if payload invalid
        if(not self.check_payload_ok(payload)):
            #end the function immediagely
            print_with_time("Got a corrupted payload: ")
            print_with_time(payload)
            #end the function
            return -1
        print_with_time("Current payload:")
        print(payload)
        print_with_time("Received a valid payload. Start to cracking password. This is going to take a long time (minutes).")
        #extract the corresponding payloads
        password_hash = payload[pw_idx]
        pw_start_range = payload[range_start_idx]
        pw_end_range = payload[range_end_idx]
        #try to find the password
        cracked_pw = self.crack_pw(password_hash,pw_start_range,pw_end_range)
        return cracked_pw

    def listen_wrapper(self, connection, encoding = encoding, debug = debug):
        res = self.start_listen(connection,encoding,debug)
        print_with_time("A worker has finished and the result sent back.")
        if(debug):
            print("listener finished with the following result")
            print(res)

        if(res == -1):
            send_msg(connection,b"-1\n")
        else:
            send_msg(connection,(res + "\n").encode(encoding))
        #close conn
        connection.close()

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
    print_with_time("Binding to port: " + str(bind_port))

#create sockert listener
def run_listener():
    # create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((bind_address, bind_port))
    except:
        print_with_time("Error on binding port! Is there a server instance already running?")
        return -1

    sock.listen()
    while(True):
        # create the incoming connection once there is one
        connection, address = sock.accept()
        newthread = SubThread(connection)
        newthread.start()
        #self.start_listen(self,bind_address,bind_port, encoding, debug)
        print_with_time('[Main] Submitted a new thread!')

    return sock

# main method
def main():
    ## initialization, accept and update global variables.
    initialize()
    #pw main thread
    run_listener()

    return




#invoke the main function
if __name__== "__main__":
    main()
