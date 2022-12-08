'''
Author: Jinqi Lu, Quansen Wang
Prof. Matta
CS 655 PA3 GENI-MINILAB
Boston University
December 8, 2022
Helper Methods for both node and mgmt
'''
from datetime import datetime
import hashlib
from string import ascii_lowercase, ascii_uppercase
from time import sleep

global_timeout = 300.0
#passwrod range
pw_range = ascii_lowercase + ascii_uppercase
sep = "<SEP>"
edge_start = "<START>"
edge_end = "<END>\n"
encoding = "utf-8"
#decode a byte string received into list of payloads
def decode_payload_into_list(payload, edge_start, edge_end, sep, encoding = "utf-8"):
    #check for payload integrity
    if(not payload.startswith(edge_start) or not payload.endswith(edge_end)):
        print_with_time("Start or end sign not matached!")
        return -1
    #remove the edges from the string first
    payload = payload[len(edge_start):len(payload) - len(edge_end)]
    return payload.split(sep)
#return a list of index for inputed string in the pw
def get_idx_list_pw(str):
    res = []
    for i in str:
        try:
            res.append(pw_range.index(i))
        except:
            res.append(-1)
    return res

#compare two index list
def compare_two_idx_list(start, end):
    for (a,b) in zip(start,end):
        if(a != b):
            return False
    return True

#check start and end index valid, the leading index of end should either equal or greater than the start
def checking_pw_range(start, end):
    for(a,b) in zip(start,end):
        if(a < b):
            return True
        elif(a == b):
            pass
        else:
            return False
    #start and end are equal
    return False
#get md5 of a inputed index list
def get_md5_from_list(idx_list):
    return get_md5(get_str_from_list(idx_list))

#get string from inputed index list
def get_str_from_list(idx_list):
    str = ""
    for i in idx_list:
        str += pw_range[i]
    return str

#check and update index list
def update_index_list(idx_list, max_int = len(pw_range)):
    #add 1 to the last element first
    idx_list[-1] = idx_list[-1] + 1
    #update the remaining element if necessary

    for i in reversed(range(len(idx_list))):
        #get the current element first
        ele = idx_list[i]
        #set to 0 if it is equals to the max_int
        if(ele == max_int):
            idx_list[i] = 0
            #update the previous one if current is not at index 0
            if(i != 0):
                idx_list[i-1] = idx_list[i-1] + 1
    return idx_list

#check if input is a valid integer within range. bounds are excluded
def is_int(input_number, check_bound = False,low = 0, up = 65536):
    try:
        res = int(input_number)
        if(check_bound):
            if(low < res < up):
                return True
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

#send provided to a given connection. it will wait [delay] amount of milisecond/ms before actually send the msg to client.
#Note: This function does not check for input validity, make sure the inputed delay is an integer
def send_msg(conn, payload, delay = 0):
    if(not is_int(delay)):
        print("Error! the provided delay is not an integer: ")
        print(delay)
        return -1
    #avoid zero division error
    if(delay == 0):
        conn.sendall(payload)
    else:
        sleep(delay/1000)
        conn.sendall(payload)
    return 0

#turn list index into integer
def idx_list_to_int(idx_list):
    let = len(pw_range)
    leni = len(idx_list)
    res = 0
    for i in range(leni):
        #get actual number
        res += idx_list[i] * let**(leni - i - 1)
    return res

#turn integer into list idx
def int_to_list_idx(num):
    let = len(pw_range)
    res = []
    while(num != 0):
        res.append(num % let)
        num //= let
    while(len(res) < 5):
        res.append(0)
    res.reverse()
    return res



