import sys
import zmq
from random import randrange
import time
import get_ip_addr as ipman
IP = ipman.get_default_addr()

print("Current libzmq version is %s" % zmq.zmq_version())
print("Current  pyzmq version is %s" % zmq.__version__)

context = zmq.Context()

socket = context.socket(zmq.REQ)


soc = context.socket (zmq.SUB)
con_str = "tcp://" + "10.0.0.6" + ":5557"
print(con_str)
soc.connect(con_str)


srv_addr = "10.0.0.1"
connect_str = "tcp://" + srv_addr + ":5555"
socket.connect (connect_str)
SUB_name = "sub_temperature"
# IP = "10.0.0.4"

while True:
    string_send = str(SUB_name + " " + IP)

    socket.send(string_send.encode())

    message = socket.recv().decode()
    print(message)
    if message == "registered":
        break


needed = "10.0.0.2"

while True:
    soc.setsockopt_string(zmq.SUBSCRIBE, needed)
    data = soc.recv_string()
    print(data)
    # time.sleep(1)
    with open('temperature.txt', 'a') as f:
        f.write(data+"\n")
        time.sleep(1)
