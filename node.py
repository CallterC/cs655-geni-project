'''
Author: Jinqi Lu & Quansen Wang
Prof. Matta
CS 655 PA3 GENI-MINILAB
Boston University
December 8, 2022
python node.py <port number>
This script runs on its own.
'''

### Import Libraries ###
import sys, socket

### Global Variables ###
script_name = "node.py"
python_head = "python"
debug = True
encoding = "utf-8"
sending_length = 1024
###payload related settings###
'''
formate of a complete payload
<edge>password_md5<SEP>calc_range_start<SEP>calc_range_end(exclusive)<SEP>check_sum<edge>
'''
sep = "<SEP>"
edge = "<edge>"
pw_idx = 0
range_start_idx = 1
range_end_idx = 2
chk_idx = 3

### Placeholder Variables ###
bind_address = "0.0.0.0"
bind_port = 9902

###Helper Methods###
#decode a byte string received into list of payloads
def decode_payload_into_list(payload, encoding = encoding):
    #decode payload
    payload = payload.decode(encoding)
    #check for payload integrity
    if(not payload.startswith(edge) or not payload.endswith(edge)):
        return -1

    #remove the edges from the string first
    payload = payload[len(edge):len(payload) - len(edge)]

    return payload.split(sep)

#check if the payload is valid
def payload_is_valid(payload):
    return
#check if input is a valid integer within range. bounds are excluded
def is_int(input_number, check_bound = False,low = 0, up = 65536):
    try:
        res = int(input_number)
        if(check_bound):
            if(low < res < up):
                return True
            else:
                return False
        else:
            return False
        return True
    except:
        return False

#initialize the global variables
def initialize():
    global bind_port, bind_address
    #Check for arguments
    if(debug):
        print("Length of arguments: " + str(len(sys.argv)))
    if(len(sys.argv) != 2):
        print("Insufficient or excess arguments! Please use " + python_head + " " + script_name + " <bind port>")
        exit(1)
    bind_port = sys.argv[1]

    #check for valid port number
    if (is_int(bind_port, True,0,65536)):
        bind_port = int(bind_port)
    else:
        print("Invalid port number! Please use INTEGER between 0 and 65535.")
        exit(1)
    if(debug):
        print("Valid port, port: " + str(bind_port))
    print("Binding to port: " + bind_port)

# main method
def main():
    #print(decode_payload_into_list(b"<edge>password_md5<SEP>calc_range_start<SEP>calc_range_end(exclusive)<SEP>check_sum<edge>"))
    ## initialization, accept and update global variables.
    initialize()
    #send and print the message
    return




#invoke the main function
if __name__== "__main__":
    main()
