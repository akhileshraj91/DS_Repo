import sys
import zmq
from random import randrange
import time
import get_ip_addr as ipman
IP = ipman.get_default_addr()



context = zmq.Context()

socket = context.socket(zmq.REQ)


soc = context.socket (zmq.SUB)
con_str = "tcp://" + "10.0.0.2" + ":5557"
print(con_str)
soc.connect(con_str)


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

while True:
    soc.setsockopt_string(zmq.SUBSCRIBE, needed)
    data = soc.recv_string()
    print(data)
    # time.sleep(1)
    with open('humidity.txt', 'a') as f:
        f.write(data+"\n")
        time.sleep(1)