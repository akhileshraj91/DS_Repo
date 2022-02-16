import sys
import zmq
from random import randrange
import useful_fns
import time

IP = useful_fns.get_default_addr()

zipcode = 37209
print("Starting the Temperature publisher for: ", zipcode)

context = zmq.Context()

socket = context.socket(zmq.REQ)


srv_addr = "10.0.0.1"
connect_str = "tcp://" + srv_addr + ":5555"
socket.connect (connect_str)
kind = "PUB"
info = "temperature"
while True:
    string_send = str(kind + " " + info + " " + IP + " " + "%i" % (zipcode))
    socket.send(string_send.encode())
    print("Attempting to register the device")

    message = socket.recv().decode()
    print(message)
    if message == "registered":
        break



soc = context.socket(zmq.PUB)
soc.bind("tcp://*:5556")
while True:
    temperature = randrange(-80, 135)
    data = temperature
    string_send = str("%i %i" % (zipcode, data))
    soc.send(string_send.encode())
    time.sleep(1)