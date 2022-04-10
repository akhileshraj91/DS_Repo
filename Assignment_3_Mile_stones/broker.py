
import sys
import zmq
import socket
import time
import json
import useful_fns
from random import randrange
args = useful_fns.parseCmdLineArgs()

def zk_main ():
    print("Registering the subscriber with zookeeper")
    parsed_args = useful_fns.parseCmdLineArgs ()
    

    client = useful_fns.ZK_ClientApp (parsed_args)

    client.init_client ()
    
    client.run_client ()
    value = None

    while value == None:
        value, stat = client.zk.get ("/MAIN/register")

        print(value.decode())

    return value.decode()



srv_addr = zk_main()
IP = useful_fns.get_default_addr()
PORT = randrange(5000,9999)
PORT = str(PORT)

context = zmq.Context()

zip_code = "37209"
socket_register = context.socket(zmq.REQ)
# srv_addr = "10.0.0.1"
connect_str = "tcp://" + srv_addr + ":5555"
socket_register.connect (connect_str)
kind = "BROKER"
parsed_args = args
subscriber =  useful_fns.CS6381_Subscriber (parsed_args)


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
        info = json.loads(json_data)
        if info and len(info) > 1:
            PUB = info[0]
            SUB = info[1]
            for s in SUB.keys():
                if s in PUB.keys():
                    lookup_dict = PUB[s]

                    subscriber.get_pubs(lookup_dict,"indirect")

                    subscriber.configure ("indirect broker")

                    subscriber.broker_loop (PORT)
                else:
                    continue
    