import zmq
from random import randrange
import socket as s1

print("Current libzmq version is %s" % zmq.zmq_version())
print("Current  pyzmq version is %s" % zmq.__version__)

context = zmq.Context()

socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")
PUB_name = "temperature"
IP = s1.gethostbyname(s1.gethostname())
print(IP.dtype() )

while True:
    zipcode = randrange(1, 100000)

    temperature = randrange(-80, 135)

    socket.send_string("%i %i PUB_name IP" % (zipcode, temperature))