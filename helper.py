'''
Author: Jinqi Lu
Prof. Matta
CS 655 PA3 GENI-MINILAB
Boston University
December 8, 2022
Helper Methods for both node and mgmt
'''
from datetime import datetime
import hashlib


global_timeout = 200.0


#decode a byte string received into list of payloads
def decode_payload_into_list(payload, edge_start, edge_end, sep, encoding = "utf-8"):
    #decode payload
    payload = payload.decode(encoding)
    #check for payload integrity
    if(not payload.startswith(edge_start) or not payload.endswith(edge_end)):
        return -1

    #remove the edges from the string first
    payload = payload[len(edge_start):len(payload) - len(edge_end)]

    return payload.split(sep)

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

def print_with_time(msg, show = True):
    msg = str(msg)
    now = datetime.now()
    prefix = "[" + now.strftime("%m/%d %H:%M:%S") + "] "
    if(show):
        print(prefix + msg)
    return prefix + msg

#receive all the information until the EOP (end of payload) signal was detected for an open connection.
def receive_all(conn, max_size = -1, eop_char = "\n", single_size = 1024, encode = "utf-8", time_out = global_timeout):
    #print(max_size,eop_char,single_size,encode,time_out)
    try:
        res = ""
        while (True):
            #set timeout in case of non properly ended string with exactly same expected size (unlikely)
            conn.settimeout(time_out)
            payload = conn.recv(single_size)
            conn.settimeout(global_timeout)
            t = payload.decode(encode)
            if(len(t) >= 1):
                if(t[-1] == eop_char):
                    res += t
                    break
                else:
                    res += t
            else:
                break
            #stop immediately if size is longer than expected
            if(max_size != -1 and not check_size_bytes(res,max_size,encode)):
                return -1
            #check if received msg is less than the single size
            #if yes, then the msg is not properly ended with EOP and is ended.
            if(len(t)<single_size):
                break
        #check one more time before return
        if (max_size != -1 and not check_size_bytes(res, max_size, encode)):
            return -1
        return res
    except:
        #timeout occured, return error
        return -1

#return false if string size in bytes is larger than provided
def check_size_bytes(sent, size, encoding):
    if(len(sent.encode(encoding)) <= size):
        return True
    else:
        return False
#get md5 of a string
def get_md5(str, encoding = "utf-8"):
    return hashlib.md5(str.encode(encoding)).hexdigest()
#calc checksum
def calc_check_sum(payload_list_no_chksum):
    str = ""
    for i in payload_list_no_chksum:
        str += i
    return get_md5(str)

#compare check sum
def check_sum_ok(payload_list):
    try:
        #assume checksum is the last element of the list
        chk = payload_list.pop()
        if(chk == calc_check_sum(payload_list)):
            return True
        else:
            return False
    except:
        return False