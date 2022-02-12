import sys
import zmq
from random import randrange
import time
import get_ip_addr as ipman
IP = ipman.get_default_addr()


Direct = 1

context = zmq.Context()

socket = context.socket(zmq.REQ)


soc1 = context.socket (zmq.SUB)
con_str = "tcp://" + "10.0.0.2" + ":5557"
soc1.connect(con_str)


srv_addr = "10.0.0.1"
connect_str = "tcp://" + srv_addr + ":5555"
socket.connect (connect_str)
kind = "SUB"
info_needed = "humidity"
zipcode = 65401

while True:
    string_send = str(kind + " " + info_needed + " " + IP + " " + "%i" % (zipcode))

    socket.send(string_send.encode())

    print("Attempting to register the subscriber")


    message = socket.recv().decode()
    print(message)
    if message == "registered":
        break


needed = str(zipcode)

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
        soc1.setsockopt_string(zmq.SUBSCRIBE, needed)
        data = soc1.recv_string()
        print(data)
        # time.sleep(1)
        with open('humidity.txt', 'a') as f:
            f.write(data+"\n")
            time.sleep(1)