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
port  = 9102














# main method
def main():
    # create socket
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the host
    conn.connect((addr, port))
    print(get_md5("594f803b380a41396ed63dca39503542     aaaaa"))
    send_msg(conn,b"<START>594f803b380a41396ed63dca39503542<SEP>     <SEP>aaaaa<SEP>8672b0c75f002ca58883ad312f6271be<END>\n")
    rec = receive_all(conn)
    print(rec)
#invoke the main function
if __name__== "__main__":
    main()
    #test()