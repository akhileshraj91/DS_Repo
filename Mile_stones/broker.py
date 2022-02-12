
import sys
import zmq
import socket
import time

context = zmq.Context()

socket = context.socket(zmq.SUB)


soc = context.socket(zmq.PUB)
soc.bind("tcp://*:5557")



filename = 'register.txt'
while True:
    with open(filename) as f:
        for line in f:
            words = line.split()
            if words[0] == "PUB":
                srv_addr = words[2]
                connect_str = "tcp://" + srv_addr + ":5556"
                socket.connect(connect_str)
                socket.setsockopt_string(zmq.SUBSCRIBE, words[-1])
                data = socket.recv_string()
                data_1, data_2 = data.split()
                print(data)
                with open(filename) as f2:
                    for l in f2:
                        W = l.split()
                        if W[0] == "SUB":
                            print(data_1, data_2)
                            string_send = str(data_1 + " " + data_2 + " ")
                            soc.send(string_send.encode())
                            time.sleep(1)






