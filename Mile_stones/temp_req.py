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

socket_broker = context.socket (zmq.SUB)



kind = "SUB"
info_needed = "temperature"
zipcode = 37209

while True:
    string_send = str(kind + " " + info_needed + " " + IP + " " + "%i" % (zipcode))
    socket_register.send(string_send.encode())
    print("Attempting to register the", kind)
    message = socket_register.recv().decode()
    print(message)
    if message == "registered":
        break

needed = str(zipcode)
broker_flag = 0

while True:
    print("executing loop")
    if not broker_flag:
        string_send = str("BROKER_Q")
        socket_register.send(string_send.encode())
        json_data = socket_register.recv_json()
        broker_details = json.loads(json_data)
        # print(broker_details)
        broker_ip = broker_details[0]
        broker_PORT = broker_details[1]
        # print(broker_ip, broker_PORT)
        broker_flag = 1
        connect_str = "tcp://" + broker_ip + ":" + broker_PORT
        socket_broker.connect(connect_str)

    print(needed)        
    socket_broker.setsockopt_string(zmq.SUBSCRIBE, needed)
    print("waiting for data")
    data = socket_broker.recv_string()
    print(data)
    # time.sleep(1)
    with open('temperature.txt', 'a') as f:
        f.write(data+"\n")
        time.sleep(1)
            
