
import zmq
import useful_fns
import json
import asyncio
import time

# kad_client = useful_fns.KademliaClient(4321, [("10.0.0.1",4001), ("10.0.0.2",4001), ("10.0.0.2", 4002)])
kad_client = useful_fns.KademliaClient(8468, [("10.0.0.1",8468), ("10.0.0.2",8468), ("10.0.0.2", 4002)])



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

print("going to execute the %s strategy"%strat)
print(args)
if strat == "direct":

    while True:
        message = socket_register.recv()
        words = message.decode().split()
        # if words[0] == "DHT":
        #     print("Received request to register a DHT server")
        #     message = "registered " + strat
        #     socket_register.send(message.encode())
        #     time.sleep(1)
        #     print(words)
        #     asyncio.run(useful_fns.set_main(words[0], words[1:]))
        #     print("DHT_server %s successfully registered" % words[1])

        if words[0] == "PUB":
            print("Received request to register a %s publishing %s values from the zipcode %s"%(words[0],words[1],words[-1]))
            # kad_client.set(words[0],words[1:])
            kad_client.set(words[2],words[1])
            message = "registered " + strat
            socket_register.send(message.encode())
            print("Publsiher %s successfully registered"%words[1])
            
        elif words[0] == "SUB":
            kad_client.set(words[0],words[1])
            message = "registered " + strat
            socket_register.send(message.encode())
            print("Subscriber %s successfully registered"%words[1])
            
        elif words[0] == "BROKER":
            asyncio.run(useful_fns.set_main(words[0],words[1:]))
            message = "registered " + strat
            socket_register.send(message.encode())
            print("Broker successfully registered")

        elif words[0] == "BROKER_Q":
            broker_details = asyncio.run(useful_fns.get_main(words[0]))
            data = json.dumps(broker_details)
            # print(data)
            socket_register.send_json(data)

        elif words[0] == "QUERY":
            details = asyncio.run(useful_fns.get_main(words[0]))
            data = json.dumps(details)
            socket_register.send_json(data)

        else:
            continue

elif strat == "indirect":


    while True:

        message = socket_register.recv()

        words = message.decode().split()

        # print(words)

        if words[0] == "PUB":
            print("Received request to register a %s publishing %s values from the zipcode %s"%(words[0],words[1],words[-1]))
            publishers[words[1]] = words[2]
            message = "registered " + strat
            socket_register.send(message.encode())
            print("Publsiher %s successfully registered"%words[1])
            
        elif words[0] == "SUB":
            subscribers[words[1]] = words[2]
            message = "registered " + strat
            socket_register.send(message.encode())
            print("Subscriber %s successfully registered"%words[1])
            
        elif words[0] == "BROKER":
            broker_details[words[1]] = "hit"
            message = "registered " + strat
            socket_register.send(message.encode())
            print("Broker successfully registered")            

        
        elif words[0] == "QUERY":
            data = json.dumps({"p":publishers, "s":subscribers})
            socket_register.send_json(data)


        elif words[0] == "BROKER_Q":
            data = json.dumps(broker_details)
            print(data)
            socket_register.send_json(data)
            print(broker_details)

else:
    print("wrong strategy")
