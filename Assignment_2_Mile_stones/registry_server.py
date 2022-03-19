
import zmq
import useful_fns
import json
import asyncio
import time


IP = useful_fns.get_default_addr()

print("Registry started running on the server address: ", IP)

context = zmq.Context ()  

socket_register = context.socket (zmq.REP)

socket_register.bind ("tcp://*:5555")

publishers = {}
subscribers = {}
broker_details = {}
args = useful_fns.parseCmdLineArgs()

strat = args.strategy


kad_client = useful_fns.KademliaClient(8468, [("10.0.0.1",8468), ("10.0.0.2",8468), ("10.0.0.2", 4002)])

print("going to execute the %s strategy"%strat)
print(args)
if strat == "direct":

    while True:
        print("executing loop")
        # print("$$$$$$$$$ looping")
        message = socket_register.recv()
        print(message)
        words = message.decode().split()

        if words[0] == "PUB":
            print("Received request to register a %s publishing %s values from the zipcode %s"%(words[0],words[1],words[-1]))
            if words[2] in publishers.keys():
                publishers[words[2]].append(words[1])
                print("the repo was already present")
            else:
                publishers[words[2]] = []
                publishers[words[2]].append(words[1])
                print("the repo was just created")

            kad_client.set("PUB",json.dumps(publishers))
            message = "registered " + strat
            socket_register.send(message.encode())
            print("Publsiher %s successfully registered"%words[1])
            
        elif words[0] == "SUB":
            if words[2] in subscribers.keys():
                subscribers[words[2]].append(words[1])
                print("the repo was already present")
            else:
                subscribers[words[2]] = []
                subscribers[words[2]].append(words[1])
                print("the repo was just created")
            kad_client.set("SUB",json.dumps(subscribers))
            message = "registered " + strat
            socket_register.send(message.encode())
            print("Subscriber %s successfully registered"%words[1])


        elif words[0] == "QUERY":
            details = kad_client.get("PUB")
            print(words[1], publishers.keys())
            if words[1] in publishers.keys():
                data = json.loads(details)[words[1]]
            else:
                data = None
            print(".........................................................",data)
            socket_register.send_json(json.dumps(data))

        elif words[0] == "remove":
            # if words[2] in publishers.keys():
            #     publishers[words[2]].remove(words[1])
            #     print("the publisher is removed")
            #     print(publishers)
            #     kad_client.set("PUB",json.dumps(publishers))
            #     details = kad_client.get("PUB")
            #     data = json.loads(details)[words[2]]
            #     print("###",data)
            #     # data = "empty"
            #     socket_register.send(data.encode())
            #     time.sleep(0.5)
            #     print("********")
            #     # continue

            print("Received request to %s a publisher publishing %s values from the zipcode %s"%(words[0],words[1],words[-1]))
            if words[2] in publishers.keys():
                publishers[words[2]].remove(words[1])
                print("............................",publishers)

            #     publishers[words[2]].append(words[1])
            #     print("the repo was already present")
            # else:
            #     publishers[words[2]] = []
            #     publishers[words[2]].append(words[1])
            #     print("the repo was just created")

            kad_client.set("PUB",json.dumps(publishers))
            message = "removed " + strat
            socket_register.send(message.encode())
            print("Publsiher %s successfully removed"%words[1])

            # details = kad_client.get("PUB")
            # if words[1] in publishers.keys():
            #     data = json.loads(details)[words[1]]
            # else:
            #     data = None
            # print(data)
            # socket_register.send_json(json.dumps(data))



            # continue

elif strat == "indirect":


    while True:

        message = socket_register.recv()

        words = message.decode().split()

        # print(words)
        if words[0] == "PUB":
            print("Received request to register a %s publishing %s values from the zipcode %s"%(words[0],words[1],words[-1]))
            if words[2] in publishers.keys():
                publishers[words[2]].append(words[1])
                print("the repo was already present")
            else:
                publishers[words[2]] = []
                publishers[words[2]].append(words[1])
                print("the repo was just created")

            kad_client.set("PUB",json.dumps(publishers))
            message = "registered " + strat
            socket_register.send(message.encode())
            print("Publsiher %s successfully registered"%words[1])
            
        elif words[0] == "SUB":
            if words[2] in subscribers.keys():
                subscribers[words[2]].append(words[1])
                print("the repo was already present")
            else:
                subscribers[words[2]] = []
                subscribers[words[2]].append(words[1])
                print("the repo was just created")
            kad_client.set("SUB",json.dumps(subscribers))
            message = "registered " + strat
            socket_register.send(message.encode())
            print("Subscriber %s successfully registered"%words[1])

        elif words[0] == "QUERY":
            details = kad_client.get("PUB")
            print(words[1], publishers.keys())
            if words[1] in publishers.keys():
                data = json.loads(details)[words[1]]
            else:
                data = None
            print(".........................................................",data)
            socket_register.send_json(json.dumps(data))
            
        elif words[0] == "BROKER":
            broker_details[words[1]] = words[0]
            kad_client.set("BROKER",json.dumps(broker_details))
            message = "registered " + strat
            socket_register.send(message.encode())
            print("Broker successfully registered")            

        elif words[0] == "BROKER_Q":
            broker_details = kad_client.get("BROKER")
            data = broker_details
            socket_register.send_json(data)
            print(broker_details)

else:
    print("wrong strategy")
