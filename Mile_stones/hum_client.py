import sys
import zmq
from random import randrange
import time
import get_ip_addr as ipman

# zipcode = randrange(1, 100000)
zipcode = 65401

IP = ipman.get_default_addr()

print("Starting the Humidity publisher for: ", zipcode)


context = zmq.Context()

socket = context.socket(zmq.REQ)


srv_addr = "10.0.0.1"
connect_str = "tcp://" + srv_addr + ":5555"
socket.connect (connect_str)
kind = "PUB"
info = "humidity"

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
PUB_name = "humidity"
while True:
    humidity = randrange(10, 60)
    data = humidity
    string_send = str("%i %i" % (zipcode, data))
    soc.send(string_send.encode())