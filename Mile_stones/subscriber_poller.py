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
info = "temperature"
while True:
    string_send = str(kind + " " + info + " " + IP + ":" + PORT + " " + zip_code)
    socket_register.send(string_send.encode())
    print("Attempting to register the device")

    message = socket_register.recv().decode()
    cm = message.split()
    if cm[0] == "registered":
        print(cm[0])
        break


string_send = str("QUERY_all")
socket_register.send(string_send.encode())
json_data = socket_register.recv_json()
lookup_dict = json.loads(json_data)
print(lookup_dict['p'])
required_addresses = useful_fns.get_key(zip_code, lookup_dict['p'])
print(required_addresses)
    
def main ():
    parsed_args = useful_fns.parseCmdLineArgs ()

    subscriber =  useful_fns.CS6381_Subscriber (parsed_args)

    subscriber.configure (required_addresses)

    subscriber.event_loop (required_addresses)
    
#----------------------------------------------
if __name__ == '__main__':
    main ()
