import zmq
from random import randrange
import socket
print("Current libzmq version is %s" % zmq.zmq_version())
print("Current  pyzmq version is %s" % zmq.__version__)

context = zmq.Context()

socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

while True:
    zipcode = randrange(1, 100000)

    relhumidity = randrange(10, 60)

    socket.send_string("%i %i" % (zipcode, temperature, relhumidity))