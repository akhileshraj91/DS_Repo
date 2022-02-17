import sys
import zmq
from random import randrange
import useful_fns
import time

IP = useful_fns.get_default_addr()
PORT = "5556"
zipcode = 37209
print("Starting the Temperature publisher for: ", zipcode)

context = zmq.Context()

socket_register = context.socket(zmq.REQ)


srv_addr = "10.0.0.1"
connect_str = "tcp://" + srv_addr + ":5555"
socket_register.connect (connect_str)
kind = "PUB"
info = "temperature"
while True:
    string_send = str(kind + " " + info + " " + IP + ":" + PORT + " " + "%i" % (zipcode))
    socket_register.send(string_send.encode())
    print("Attempting to register the device")

    message = socket_register.recv().decode()
    cm = message.split()
    if cm[0] == "registered":
        print(cm[0])
        break



socket_pub = context.socket(zmq.PUB)
socket_pub.bind("tcp://*:"+PORT)
while True:
    temperature = randrange(-80, 135)
    data = temperature
    string_send = str("%i %i" % (zipcode, data))
    socket_pub.send(string_send.encode())
    time.sleep(1)