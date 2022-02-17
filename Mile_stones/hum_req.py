import sys
import zmq
from random import randrange
import time
import useful_fns
import json
IP = useful_fns.get_default_addr()


Direct = 0

context = zmq.Context()

socket_register = context.socket(zmq.REQ)
srv_addr = "10.0.0.1"
connect_str = "tcp://" + srv_addr + ":5555"
socket_register.connect (connect_str)

socket_broker = context.socket (zmq.SUB)



kind = "SUB"
info_needed = "humidity"
zipcode = 65401

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

if Direct:
    soc1.setsockopt_string(zmq.SUBSCRIBE, needed)
    data = soc1.recv_string()
    print(data)
    zipcode, source_ip = data.split()
    # time.sleep(1)
    while True:
        soc2 = context.socket (zmq.SUB)
        con_str = "tcp://" + source_ip + ":5556"
        soc2.connect(con_str)
        soc2.setsockopt_string(zmq.SUBSCRIBE, needed)
        data = soc2.recv_string()
        print(data)
        with open('humidity.txt', 'a') as f:
            f.write(data+"\n")
            time.sleep(1)

else:

    while True:
        # print("executing loop")
        if not broker_flag:
            string_send = str("BROKER_Q")
            socket_register.send(string_send.encode())
            json_data = socket_register.recv_json()
            broker_details = json.loads(json_data)
            print(broker_details)
            # broker_ip = broker_details[0]
            # broker_PORT = broker_details[1]
            broker_flag = 1
            connect_str = "tcp://" + broker_details
            socket_broker.connect(connect_str)

        socket_broker.setsockopt_string(zmq.SUBSCRIBE, needed)
        data = socket_broker.recv_string()
        print(data)
        # time.sleep(1)
        with open('humidity.txt', 'a') as f:
            f.write(data+"\n")
            time.sleep(1)