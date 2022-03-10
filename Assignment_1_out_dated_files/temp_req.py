import sys
import zmq
from random import randrange
import time
import useful_fns
import json

IP = useful_fns.get_default_addr()


context = zmq.Context()

socket_register = context.socket(zmq.REQ)
srv_addr = "10.0.0.1"
connect_str = "tcp://" + srv_addr + ":5555"
socket_register.connect (connect_str)

socket_list = context.socket (zmq.SUB)



kind = "SUB"
info_needed = "temperature"
zipcode = 37209

while True:
    string_send = str(kind + " " + info_needed + " " + IP + " " + "%i" % (zipcode))
    socket_register.send(string_send.encode())
    print("Attempting to register the", kind)
    message = socket_register.recv().decode()
    cm = message.split()
    if cm[0] == "registered":
        print(cm[0])
        break

needed = str(zipcode)
broker_flag = 0

if cm[1] == "indirect":

    while True:
        if not broker_flag:
            string_send = str("BROKER_Q")
            socket_register.send(string_send.encode())
            json_data = socket_register.recv_json()
            broker_details = json.loads(json_data)
            print(broker_details)
            # broker_ip = broker_details[0]
            # broker_PORT = broker_details[1]
            # print(broker_ip, broker_PORT)
            broker_flag = 1
            connect_str = "tcp://" + broker_details
            socket_list.connect(connect_str)

        print(needed)        
        socket_list.setsockopt_string(zmq.SUBSCRIBE, needed)
        print("waiting for data")
        data = socket_list.recv_string()
        print(data)
        # time.sleep(1)
        with open('temperature.txt', 'a') as f:
            f.write(data+"\n")
        time.sleep(1)
            
else:
    while True:
        string_send = str("QUERY")
        socket_register.send(string_send.encode())
        json_data = socket_register.recv_json()
        lookup = json.loads(json_data)
        for k in lookup.keys():
            if k == "tp":
                for key in lookup[k].keys():
                    if lookup[k][key] == needed:
                        srv_addr = key
                        connect_str = "tcp://" + srv_addr
                        socket_list.connect(connect_str)
                        socket_list.setsockopt_string(zmq.SUBSCRIBE, lookup[k][key])
                        data = socket_list.recv_string()
                        data_1, data_2 = data.split()
        socket_list.setsockopt_string(zmq.SUBSCRIBE, needed)
        print("waiting for data")
        data = socket_list.recv_string()
        print(data)
        # time.sleep(1)
        with open('temperature.txt', 'a') as f:
            f.write(data+"\n")
        time.sleep(1)
