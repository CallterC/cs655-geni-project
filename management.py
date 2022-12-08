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
import datetime
from helper import *
from flask import Flask, render_template, request, redirect, url_for
from hosts import *
collected_results = []

#def assemble sinlge payload
def create_single_payload(start, end, hash, encoding = encoding):
    checksum = get_md5(hash + start + end)
    return (edge_start + hash + sep + start + sep + end + sep + checksum + edge_end).encode(encoding)

#create specified number of payloads.
def create_all_payloads(hash, number, encoding = encoding):
    print_with_time("Assigning jobs...")
    lenp = len(pw_range)
    low_bound = 0
    high_bound = lenp ** 5 -1
    res = []
    #get approx bin
    bin = high_bound // number
    start = 0
    for i in range(number):
        if(start + bin + 1 < high_bound):
            res.append([start, start + bin])
            start += bin
        else:
            res.append([start, high_bound])
    pay = []
    for i in res:
        st = get_str_from_list(int_to_list_idx(i[0]))
        ed = get_str_from_list(int_to_list_idx(i[1]))
        pay.append(create_single_payload(st, ed, hash,encoding))
    return pay

#run jobs
def run_single_job(host, port, payload, timeout):
    global collected_results
    #create socket and connect to it
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the host
    conn.connect((host, port))
    #send payload
    send_msg(conn,payload)
    #get result
    res = receive_all(conn, 1024, "\n", 1024, encoding, timeout)
    collected_results.append(res)
    #close connection
    conn.close()
    #return result
    return res

#I trust the assigned number will NOT BE LARGER than the nummber of hosts
def run_jobs(hash, number, timeout, encoding = encoding):
    job_list = create_all_payloads(hash, number, encoding)
    tlist = []
    print_with_time("Creating threads...")
    for i in range(number):
        node = hosts[i]
        job = job_list[i]
        host = node[0]
        port = node[1]
        #create thread
        threadX = threading.Thread(target=run_single_job, args=(host, port, job, timeout))
        #add to thread list
        tlist.append(threadX)
    print_with_time("Running... This is going to take a long time")
    print_with_time("Global timeout: " + str(timeout) + " seconds...")
    #start the threads and collect results
    for i in tlist:
        i.start()
    #collect the result
    for i in tlist:
        i.join()
    print_with_time("Job finished...")

#analyze results
def get_result_str():
    global collected_results
    print(collected_results)
    tio = False
    for i in collected_results:
        if(i != "-1\n" and i != -1):
            return i[:-1]
        if(i == -1):
            print("Timeout")
            tio = True
    res = "No matched result found. Maybe the hash you provided is not in the range? "
    if(tio):
        res += "Some nodes has timed out, you may want to check your timeout settings."
    ##reset the global list
    collected_results = []
    return res

#run cracker
def crack(provided_hash, provided_host_num, timeout, encoding = encoding):
    #run jobs
    run_jobs(provided_hash, provided_host_num, timeout, encoding)
    #analyze results
    return get_result_str()

# # main method
# def main():
#     # ZZZZY
#     provided_hash = "28ab351202b4d41d3fb4b368e3b544ac"
#     # provided number of hosts number
#     provided_host_num = 5
#     #time out value in seconds
#     time_out = 300
#     if(provided_host_num > len(hosts)):
#         print("Rejected, provided number of working nodes is greater than what limit.")
#         return
#     start = datetime.now()
#     print(crack(provided_hash, provided_host_num, time_out, encoding))
#     end = datetime.now()
#     print("Total running time: ")
#     print(end - start)


app = Flask(__name__)
@app.route('/', methods=('GET', 'POST'))

def index(): 
    md5 = None
    numWorkers = None
    tVal = None
    res = None
    time = None
    if request.method == 'POST':
        md5 = request.form['md5']
        numWorkers = request.form['workerNum']
        tVal = request.form['timeoutVal']
        if(is_int(numWorkers)):
            numWorkers = int(numWorkers)
        else:
            return render_template('index.html', pwd="Invalid input, please use integer for number of workers", timeTaken=time)
        if (is_int(tVal)):
            tVal = int(tVal)
        else:
            return render_template('index.html', pwd="Invalid input, please use integer for timeout value", timeTaken=time)

        res = crack(md5, numWorkers, tVal, encoding)
    # commented for debug purposes, the 
    # time out value in seconds
    # time_out = 300
    # if(is_int(numWorkers)):
    #     numWorkers = int(numWorkers)
    # else:
    #     print("Rejected, provide only integer number of working nodes...")
    # print(type(numWorkers))
    # if(numWorkers > len(hosts)):
    #     print("Rejected, provided number of working nodes is greater than what limit.")
    #     return
    # start = datetime.now()
    # res = crack(md5, numWorkers, time_out, encoding)
    # end = datetime.now()
    # time = str(end - start)

    return render_template('index.html', pwd=res, timeTaken=time)


if __name__ == '__main__':
    app.run(debug=True)