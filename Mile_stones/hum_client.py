import sys
import zmq
from random import randrange
import time
import useful_fns

zipcode = 65401

IP = useful_fns.get_default_addr()
PORT = "5556"
print("Starting the Humidity publisher for: ", zipcode)

context = zmq.Context()

socket_register = context.socket(zmq.REQ)

srv_addr = "10.0.0.1"
connect_str = "tcp://" + srv_addr + ":5555"
socket_register.connect (connect_str)
kind = "PUB"
info = "humidity"

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
socket_pub.bind("tcp://*:" + PORT)
PUB_name = "humidity"
while True:
    humidity = randrange(10, 60)
    data = humidity
    string_send = str("%i %i" % (zipcode, data))
    socket_pub.send(string_send.encode())
    time.sleep(1)