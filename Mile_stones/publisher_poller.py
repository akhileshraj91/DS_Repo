
import sys
import time
import zmq
from random import randrange
import useful_fns
import json
import random

args = useful_fns.parseCmdLineArgs()

zip_code = args.zipcode

IP = useful_fns.get_default_addr()
PORT = randrange(5000,9999)
PORT = str(PORT)


context = zmq.Context()
socket_register = context.socket(zmq.REQ)
srv_addr = "10.0.0.1"
connect_str = "tcp://" + srv_addr + ":5555"
socket_register.connect (connect_str)
kind = "PUB"
while True:
    string_send = str(kind + " " + IP + ":" + PORT + " " + zip_code)
    print(string_send)
    socket_register.send(string_send.encode())
    print("Attempting to register the device")

    message = socket_register.recv().decode()
    cm = message.split()
    if cm[0] == "registered":
        print(cm[0])
        break



bind_str = "tcp://*:"+PORT

socket = context.socket (zmq.PUB)
socket.bind (bind_str)

params = args.info.split(",")
print(params)
while True:
    para = random.choice(params)
    if para == "temp":  # temp
        temp = randrange (-10, 101)
        topic = "temp:" + " " + zip_code + " " + str (temp)+ " " + str(time.time()) 
    elif para == "humidity": # humidity
        humidity = randrange (20, 101)
        topic = "humidity:" + " " + zip_code + " " + str (humidity)+ " "+ str(time.time())
    elif para == "pressure": # pressure
        pressure = randrange (26, 34)
        topic = "pressure:" + " " + zip_code + " " + str (pressure)+ " " + str(time.time())
    else:
        print ("bad category")
        continue

    print ("Sending: {}".format (topic))
    socket.send_string (topic)
    time.sleep (0.5)  
