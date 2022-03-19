import sys
import argparse   # argument parser
import zmq
import useful_fns
from random import randrange
import json

def main ():
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

    parsed_args = args
    subscriber =  useful_fns.CS6381_Subscriber (parsed_args)

    if cm[1] == "direct":

        while True:
            string_send = str("QUERY"+" "+zip_code)
            print(string_send)
            socket_register.send(string_send.encode())
            json_data = socket_register.recv_json()
            print(json_data)
            lookup_dict = json.loads(json_data)
            print(".........",lookup_dict)
            if lookup_dict != None:
                subscriber.addresses = []

                subscriber.get_pubs(lookup_dict)

                subscriber.configure ()

                subscriber.event_loop ()

    elif cm[1] == "indirect":

        string_send = str("BROKER_Q")
        socket_register.send(string_send.encode())
        json_data = socket_register.recv_json()
        broker_add = json.loads(json_data)
        

        # subscriber =  useful_fns.CS6381_Subscriber (parsed_args)
        print(broker_add)

        subscriber.get_pubs(broker_add, cm[1])

        subscriber.configure ()

        subscriber.event_loop ()

    
#----------------------------------------------
if __name__ == '__main__':
    main ()
