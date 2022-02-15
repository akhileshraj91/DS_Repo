

import time
import zmq    
import get_ip_addr as ipman
IP = ipman.get_default_addr()

print("Registry started running on the server address: ", IP)

context = zmq.Context ()  

socket = context.socket (zmq.REP)

socket.bind ("tcp://*:5555")
temp_pub = {}
humd_pub = {}

temp_sub = {}
humd_sub = {}

while True:

    message = socket.recv()

    words = message.decode().split()

    print("Received request to register a %s publishing %s values from the zipcode %s"%(words[0],words[1],words[-1]))


    if words[0] == "PUB":
        if words[1] == "temperature":
            if words[-1] not in temp_pub.keys():
                temp_pub[words[-1]] = words[-2]
                print("temperature dictionary is: ", temp_pub)
                with open('register.txt', 'a') as f:
                    f.write(message.decode()+"\n")
        elif words[1] == "humidity":
            if words[-1] not in humd_pub.keys():
                humd_pub[words[-1]] = words[-2]
                print("humidity dictionary is: " , humd_pub)
                with open('register.txt', 'a') as f:
                    f.write(message.decode()+"\n")

    
    elif words[0] == "SUB":
        if words[1] == "temperature":
            if words[-1] not in temp_sub.keys():
                temp_pub[words[-1]] = words[-2]
                print("temperature dictionary is: ", temp_sub)
                with open('register.txt', 'a') as f:
                    f.write(message.decode()+"\n")
        elif words[1] == "humidity":
            if words[-1] not in humd_sub.keys():
                humd_pub[words[-1]] = words[-2]
                print("humidity dictionary is: " , humd_pub)
                with open('register.txt', 'a') as f:
                    f.write(message.decode()+"\n")


    socket.send(b"registered")
    print(words[0] + " succesfully registered")

