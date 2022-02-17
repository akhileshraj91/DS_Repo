
import sys
import zmq
import socket
import time
import json
import useful_fns
from random import randrange


IP = useful_fns.get_default_addr()
PORT = randrange(5000,9999)
PORT = str(PORT)

context = zmq.Context()


socket_register = context.socket(zmq.REQ)
srv_addr = "10.0.0.1"
connect_str = "tcp://" + srv_addr + ":5555"
socket_register.connect (connect_str)
kind = "BROKER"
while True:
    string_send = str(kind + " " + IP + ":" + PORT)

    socket_register.send(string_send.encode())
    print("Attempting to register the ", kind)

    message = socket_register.recv().decode()
    print(message)
    cm = message.split()
    if cm[0] == "registered":
        break

socket_list = context.socket(zmq.SUB)

socket_broker = context.socket(zmq.PUB)
socket_broker.bind("tcp://*:" + PORT)

print(cm[1])

if cm[1] == "indirect":
    while True:
        try:
            string_send = str("QUERY")
            socket_register.send(string_send.encode())
            json_data = socket_register.recv_json()
            lookup = json.loads(json_data)
            # print(lookup)
            
            for k in lookup.keys():
                if k == "tp" or k == "hp":
                    for key in lookup[k].keys():
                        srv_addr = key
                        connect_str = "tcp://" + srv_addr
                        socket_list.connect(connect_str)
                        socket_list.setsockopt_string(zmq.SUBSCRIBE, lookup[k][key])
                        data = socket_list.recv_string()
                        data_1, data_2 = data.split()
                        # print(data)
                        print(k)
                        # for L in lookup.keys():
                        if k == "tp":
                            # print(lookup[k])
                            # print(data)
                            for key in lookup["ts"].keys():
                                print(data)
                                string_send = str(data_1 + " " + data_2 + " ")
                                socket_broker.send(string_send.encode())
                                # print(".........................",string_send)
                                time.sleep(1)
                        elif k == "hp":
                            # print(lookup[k])
                            # print(data)
                            for key in lookup["hs"].keys():
                                print(data)
                                string_send = str(data_1 + " " + data_2 + " ")
                                socket_broker.send(string_send.encode())
                                # print(".........................",string_send)
                                time.sleep(1)

        except KeyboardInterrupt:
            print("key_pressed and therefore break the loop")
            break







