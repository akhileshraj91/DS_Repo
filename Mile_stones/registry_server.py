

import time
import zmq    
import useful_fns
import json

IP = useful_fns.get_default_addr()

print("Registry started running on the server address: ", IP)

context = zmq.Context ()  

socket_register = context.socket (zmq.REP)

socket_register.bind ("tcp://*:5555")
temp_pub = {}
humd_pub = {}
publishers = {}
subscribers = {}

temp_sub = {}
humd_sub = {}
broker_details = None
args = useful_fns.parseCmdLineArgs()
strat = args.strategy


if strat == "indirect":

    while True:

        message = socket_register.recv()
        print(message)

        words = message.decode().split()

        # print(words)

        if words[0] == "PUB":
            print("Received request to register a %s publishing %s values from the zipcode %s"%(words[0],words[1],words[-1]))
            publishers[words[-2]] = words[-1] 
            if words[1] == "temperature":
                if words[-2] not in temp_pub.keys():
                    temp_pub[words[-2]] = words[-1]
                    print("temperature dictionary is: ", temp_pub)
                    with open('register.txt', 'a') as f:
                        f.write(message.decode()+"\n")
                    message = "registered " + strat
                    socket_register.send(message.encode())
            elif words[1] == "humidity":
                if words[-2] not in humd_pub.keys():
                    humd_pub[words[-2]] = words[-1]
                    print("humidity dictionary is: " , humd_pub)
                    with open('register.txt', 'a') as f:
                        f.write(message.decode()+"\n")
                    message = "registered " + strat
                    socket_register.send(message.encode())    
        
        elif words[0] == "SUB":
            subscribers[words[-2]] = words[-1]
            print("Received request to register a %s requesting %s values from the zipcode %s"%(words[0],words[1],words[-1]))

            if words[1] == "temperature":
                if words[-2] not in temp_sub.keys():
                    temp_sub[words[-2]] = words[-1]
                    print("temperature dictionary is: ", temp_sub)
                    with open('register.txt', 'a') as f:
                        f.write(message.decode()+"\n")
                    message = "registered " + strat
                    socket_register.send(message.encode())
            elif words[1] == "humidity":
                if words[-2] not in humd_sub.keys():
                    humd_sub[words[-2]] = words[-1]
                    print("humidity dictionary is: " , humd_pub)
                    with open('register.txt', 'a') as f:
                        f.write(message.decode()+"\n")
                    message = "registered " + strat
                    socket_register.send(message.encode())

        elif words[0] == "BROKER":
            broker_details = words[1]
            print(broker_details)
            message = "registered " + strat
            socket_register.send(message.encode())
            print("Broker successfully registered")            

        
        elif words[0] == "QUERY":
            data = json.dumps({"tp":temp_pub, "ts":temp_sub, "hp":humd_pub, "hs":humd_sub})
            socket_register.send_json(data)
            # print("disctionary sent")


        elif words[0] == "BROKER_Q":
            data = json.dumps(broker_details)
            # print(data)
            socket_register.send_json(data)

        elif words[0] == "QUERY_all":
            data = json.dumps({"p":publishers, "s":subscribers})
            socket_register.send_json(data)

else:


    while True:

        message = socket_register.recv()

        words = message.decode().split()

        # print(words)

        if words[0] == "PUB":
            print("Received request to register a %s publishing %s values from the zipcode %s"%(words[0],words[1],words[-1]))

            if words[1] == "temperature":
                if words[-2] not in temp_pub.keys():
                    temp_pub[words[-2]] = words[-1]
                    print("temperature dictionary is: ", temp_pub)
                    with open('register.txt', 'a') as f:
                        f.write(message.decode()+"\n")
                    message = "registered " + strat
                    socket_register.send(message.encode())
            elif words[1] == "humidity":
                if words[-2] not in humd_pub.keys():
                    humd_pub[words[-2]] = words[-1]
                    print("humidity dictionary is: " , humd_pub)
                    with open('register.txt', 'a') as f:
                        f.write(message.decode()+"\n")
                    message = "registered " + strat
                    socket_register.send(message.encode())   
        
        elif words[0] == "SUB":
            print("Received request to register a %s requesting %s values from the zipcode %s"%(words[0],words[1],words[-1]))

            if words[1] == "temperature":
                if words[-2] not in temp_sub.keys():
                    temp_sub[words[-2]] = words[-1]
                    print("temperature dictionary is: ", temp_sub)
                    with open('register.txt', 'a') as f:
                        f.write(message.decode()+"\n")
                    message = "registered " + strat
                    socket_register.send(message.encode())
            elif words[1] == "humidity":
                if words[-2] not in humd_sub.keys():
                    humd_sub[words[-2]] = words[-1]
                    print("humidity dictionary is: " , humd_pub)
                    with open('register.txt', 'a') as f:
                        f.write(message.decode()+"\n")
                    message = "registered " + strat
                    socket_register.send(message.encode())


        elif words[0] == "BROKER":
            broker_details = words[1]
            print(broker_details)
            print(strat)
            message = "registered " + strat
            socket_register.send(message.encode())
            print("Broker successfully registered")            

        
        elif words[0] == "QUERY":
            data = json.dumps({"tp":temp_pub, "ts":temp_sub, "hp":humd_pub, "hs":humd_sub})
            socket_register.send_json(data)
            # print("disctionary sent")


        elif words[0] == "BROKER_Q":
            data = json.dumps(broker_details)
            # print(data)
            socket_register.send_json(data)

