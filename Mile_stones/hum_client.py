import sys
import zmq
from random import randrange
import time

import subprocess

#find ip

out_terminal = subprocess.check_output("ifconfig", shell=True)
out_string = out_terminal.decode()
words_actual = out_string.split()
res = words_actual.index("inet")
IP = words_actual[res+1]
print(IP)


print("Current libzmq version is %s" % zmq.zmq_version())
print("Current  pyzmq version is %s" % zmq.__version__)

context = zmq.Context()

socket = context.socket(zmq.REQ)


srv_addr = "10.0.0.1"
connect_str = "tcp://" + srv_addr + ":5555"
socket.connect (connect_str)
PUB_name = "humidity"
# IP = "10.0.0.3"

while True:
    zipcode = randrange(1, 100000)

    relhumidity = randrange(10, 60)
    string_send = str(PUB_name + " " + IP + " " + "%i %i" % (zipcode, relhumidity))

    socket.send(string_send.encode())

    message = socket.recv().decode()
    print(message)
    if message == "registered":
        break


soc = context.socket(zmq.PUB)
soc.bind("tcp://*:5556")
PUB_name = "humidity"
while True:
    zipcode = randrange(1, 100000)

    humidity = randrange(10, 60)
    string_send = str(PUB_name + " " + IP + " " + "%i %i" % (zipcode, humidity))

    soc.send(string_send.encode())