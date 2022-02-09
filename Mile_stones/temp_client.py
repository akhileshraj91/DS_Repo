import sys
import zmq
from random import randrange
import get_ip_addr as ipman
# import subprocess

# #find ip

# out_terminal = subprocess.check_output("ifconfig", shell=True)
# out_string = out_terminal.decode()
# words_actual = out_string.split()
# res = words_actual.index("inet")
# IP = words_actual[res+1]
# print(IP)

IP = ipman.get_default_addr()

print("Current libzmq version is %s" % zmq.zmq_version())
print("Current  pyzmq version is %s" % zmq.__version__)

context = zmq.Context()

socket = context.socket(zmq.REQ)


srv_addr = "10.0.0.1"
connect_str = "tcp://" + srv_addr + ":5555"
socket.connect (connect_str)
PUB_name = "temperature"
# IP = "10.0.0.2" 
while True:
    zipcode = randrange(1, 100000)

    temperature = randrange(-80, 135)
    string_send = str(PUB_name + " " + IP + " " + "%i %i" % (zipcode, temperature))

    socket.send(string_send.encode())

    message = socket.recv().decode()
    print(message)
    if message == "registered":
        break



soc = context.socket(zmq.PUB)
soc.bind("tcp://*:5556")
PUB_name = "temperature"
while True:
    zipcode = randrange(1, 100000)

    temperature = randrange(-80, 135)
    string_send = str(PUB_name + " " + IP + " " + "%i %i" % (zipcode, temperature))

    soc.send(string_send.encode())