
import sys
import zmq
import socket
import time
import json
import useful_fns
from random import randrange
args = useful_fns.parseCmdLineArgs()


IP = useful_fns.get_default_addr()
PORT = randrange(5000,9999)
PORT = str(PORT)

context = zmq.Context()


socket_register = context.socket(zmq.REQ)
srv_addr = "10.0.0.1"
connect_str = "tcp://" + srv_addr + ":5555"
socket_register.connect (connect_str)
kind = "BROKER"
while True:
    string_send = str(kind + " " + IP + ":" + PORT)

    socket_register.send(string_send.encode())
    print("Attempting to register the ", kind)

    message = socket_register.recv().decode()
    print(message)
    cm = message.split()
    if cm[0] == "registered":
        break

if cm[1] == "indirect":
    while True:
        string_send = str("QUERY")
        socket_register.send(string_send.encode())
        json_data = socket_register.recv_json()
        lookup_dict = json.loads(json_data)
        

        parsed_args = args

        subscriber =  useful_fns.CS6381_Subscriber (parsed_args)

        print(lookup_dict)

        subscriber.get_pubs(lookup_dict['p'],"indirect")

        subscriber.configure ("indirect broker")

        subscriber.broker_loop (PORT)
    