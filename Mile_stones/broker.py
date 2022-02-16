
import sys
import zmq
import socket
import time
import json

context = zmq.Context()

socket = context.socket(zmq.SUB)


soc = context.socket(zmq.PUB)
soc.bind("tcp://*:5557")

Direct = 0
filename = 'register.txt'



socket_register = context.socket(zmq.REQ)
srv_addr = "10.0.0.1"
connect_str = "tcp://" + srv_addr + ":5555"
socket_register.connect (connect_str)


if Direct:
    while True:
        try:
            with open(filename) as f:
                for line in f:
                    words = line.split()
                    if words[0] == "SUB":
                        info_req = words[-1]
                        sub_addr = words[-2]
                        print(words)
                        with open(filename) as f2:
                            for l in f2:
                                W = l.split()
                                print(W)
                                if W[0] == "PUB" and W[-1] == info_req:
                                    string_send = str(W[-1] + " " + W[-2])
                                    soc.send(string_send.encode())
                                    print("information sent: ", string_send)
                                    time.sleep(1)
                                    break
        except KeyboardInterrupt:
            break





else:
    while True:
        print("executing_loop")
        try:
            # with open(filename) as f:
            #     for line in f:
            #         words = line.split()
            #         if words[0] == "PUB":
            #             srv_addr = words[2]
            #             connect_str = "tcp://" + srv_addr + ":5556"
            #             socket.connect(connect_str)
            #             socket.setsockopt_string(zmq.SUBSCRIBE, words[-1])
            #             data = socket.recv_string()
            #             data_1, data_2 = data.split()
            #             print(data)
            #             with open(filename) as f2:
            #                 for l in f2:
            #                     W = l.split()
            #                     if W[0] == "SUB":
            #                         print(data_1, data_2)
            #                         string_send = str(data_1 + " " + data_2 + " ")
            #                         soc.send(string_send.encode())
            #                         time.sleep(1)
            string_send = str("QUERY")
            # print("sending")
            socket_register.send(string_send.encode())
            # print(string_send.encode(), "sent to register")
            json_data = socket_register.recv_json()
            lookup = json.loads(json_data)
            # print(lookup)
            
            for k in lookup.keys():
                # print(k)
                if k == "tp" or k == "hp":
                    # print(lookup[k])
                    for key in lookup[k].keys():
                        srv_addr = key
                        connect_str = "tcp://" + srv_addr + ":5556"
                        socket.connect(connect_str)
                        socket.setsockopt_string(zmq.SUBSCRIBE, lookup[k][key])
                        data = socket.recv_string()
                        data_1, data_2 = data.split()
                        print(data)
                        for L in lookup.keys():
                            if L == "ts" or L == "hs":
                                # print(lookup[k])
                                for key in lookup[L].keys():
                                    string_send = str(data_1 + " " + data_2 + " ")
                                    soc.send(string_send.encode())
                                    time.sleep(1)

            # time.sleep(1)

        except KeyboardInterrupt:
            print("key_pressed and therefore break the loop")
            break







