
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
            # print("check", line)
            words = line.split()
            if len(words) > 2:
                srv_addr = words[1]
                # print(srv_addr)
                connect_str = "tcp://" + srv_addr + ":5556"
                socket.connect(connect_str)
                socket.setsockopt_string(zmq.SUBSCRIBE, words[0])
                data = socket.recv_string()
                data_1, data_2, data_3, data_4 = data.split()
                # print(data)
                with open(filename) as f2:
                    for l in f2:
                        W = l.split()
                        if len(W) == 2:
                            print(srv_addr, data_4)
                            string_send = str(srv_addr + " " + data_4 + " ")
                            # print(string_send)
                            soc.send(string_send.encode())
                            # print("sending successful")
                            time.sleep(1)
        # print("check")






