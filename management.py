'''
Author: Jinqi Lu
Prof. Matta
CS 655 PA3 GENI-MINILAB
Boston University
December 8, 2022
python management.py
This script requires the presence of helper.py to run. All configurations are configured inside the script
'''
### Import Libraries ###
import sys, socket, threading, concurrent.futures
from datetime import datetime
from helper import *

addr = "127.0.0.1"
port = 9102







#def assemble sinlge payload
def create_single_payload(start, end, hash, encoding = encoding):
    checksum = get_md5(hash + start + end)
    return (edge_start + hash + sep + start + sep + end + sep + checksum + edge_end).encode(encoding)

#create specified number of payloads.
def create_all_payloads(hash, number, encoding = encoding):
    




# main method
def main():
    md5 = ""
    md5 = md5.lower()
    # create socket
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the host
    conn.connect((addr, port))
    msg = create_single_payload("aaaaa", "bbbbb", "12522994d50179fb741c42b1b565b0f7")
    print(msg)
    send_msg(conn,msg)
    rec = receive_all(conn)
    print(rec)
#invoke the main function
if __name__== "__main__":
    main()
    #test()