import sys
import argparse   # argument parser
import zmq
import useful_fns
from random import randrange
import json

args = useful_fns.parseCmdLineArgs()
zip_code = args.zipcode


context = zmq.Context()
IP = useful_fns.get_default_addr()
PORT = randrange(5000,9999)
PORT = str(PORT)


socket_register = context.socket(zmq.REQ)
srv_addr = "10.0.0.1"
connect_str = "tcp://" + srv_addr + ":5555"
socket_register.connect (connect_str)
kind = "SUB"
while True:
    string_send = str(kind + " " + IP + ":" + PORT + " " + zip_code)
    socket_register.send(string_send.encode())
    print("Attempting to register the device")

    message = socket_register.recv().decode()
    cm = message.split()
    if cm[0] == "registered":
        print(cm[0])
        break


string_send = str("QUERY")
socket_register.send(string_send.encode())
json_data = socket_register.recv_json()
lookup_dict = json.loads(json_data)
    
def main ():
    parsed_args = args

    subscriber =  useful_fns.CS6381_Subscriber (parsed_args)

    subscriber.get_key(lookup_dict['p'])

    subscriber.configure ()

    subscriber.event_loop ()
    
#----------------------------------------------
if __name__ == '__main__':
    main ()
