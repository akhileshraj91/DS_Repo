import sys
import zmq
from random import randrange


print("Current libzmq version is %s" % zmq.zmq_version())
print("Current  pyzmq version is %s" % zmq.__version__)

context = zmq.Context()

socket = context.socket(zmq.REQ)


srv_addr = "10.0.0.1"
connect_str = "tcp://" + srv_addr + ":5555"
socket.connect (connect_str)
PUB_name = "temperature"
IP = "10.0.0.2" 
while True:
    zipcode = randrange(1, 100000)

    temperature = randrange(-80, 135)
    string_send = str(PUB_name + " " + IP + " " + "%i %i" % (zipcode, temperature))

    # socket.send(b"%i %i %i %i" % (zipcode, temperature, PUB_name, PUB_name, ))
    socket.send(string_send.encode())

    message = socket.recv().decode()
    print(message)
    if message == "registered":
        break



# context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")
PUB_name = "temperature"
while True:
    zipcode = randrange(1, 100000)

    temperature = randrange(-80, 135)
    string_send = str(PUB_name + " " + IP + " " + "%i %i" % (zipcode, temperature))

    socket.send(string_send.encode())