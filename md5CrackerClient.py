import hashlib
import socket
import sys
import time
import itertools

HOST = ""
PORT = 5000
candidate = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def generateMD5(inputString):
    m = hashlib.md5()
    m.update
    return m.hexdigest()


if __init__ == "__main__":
    if(len(sys.argv) < 3):
        print("Usage: python md5CrackerClient.py <IP> <PORTNUM>")
        sys.exit(1)

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    with(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.connect((HOST, PORT))
        while True:
            data = s.recv(1024)
            if not data:
                break
            print("Received: " + data.decode("utf-8"))
            if(data.decode("utf-8") == "DONE"):
                break
            # if(data.decode("utf-8") == "START"):
            #     startTime = time.time()
            #     for i in itertools.product(candidate, repeat=5):
            #         if(generateMD5(i) == "e2fc714c4727ee9395f324cd2e7f331f"):
            #             print("Found: " + i)
            #             break
            #     endTime = time.time()
            #     print("Time: " + str(endTime - startTime))
            #     s.sendall("DONE".encode("utf-8"))
            hash_range, hash_value = data.decode("utf-8").split("/")
            startTime = time.time()
            res = ""
            for i in itertools.product(hash_range, repeat=5):
                if(generateMD5(i) == hash_value):
                    print("Found: " + i)
                    res = i
                    break
            endTime = time.time()
            print("Time: " + str(endTime - startTime))
            s.sendall(res.encode("utf-8"))
    