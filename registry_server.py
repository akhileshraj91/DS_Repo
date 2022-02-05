

import time
import zmq    

print("Current libzmq version is %s" % zmq.zmq_version())
print("Current  pyzmq version is %s" % zmq.__version__)

context = zmq.Context ()  

socket = context.socket (zmq.REP)

socket.bind ("tcp://*:5555")
temp_pub = {}
humd_pub = {}

temp_sub = {}
humd_sub = {}

while True:

    message = socket.recv()
    print("Received request: %s" % message)

    words = message.split()



    if words[0].decode() == "temperature":
        if words[1].decode() not in temp_pub.keys():
            temp_pub[words[1].decode()] = words[1].decode()
            print("temperature dictionary is: ", temp_pub)
            with open('register.txt', 'a') as f:
                f.write(message.decode()+"\n")
    elif words[0].decode() == "humidity":
        if words[1].decode() not in humd_pub.keys():
            humd_pub[words[1].decode()] = words[1].decode()
            print("humidity dictionary is: " , humd_pub)
            with open('register.txt', 'a') as f:
                f.write(message.decode()+"\n")

    
    elif words[0].decode() == "sub_temperature":
        if words[1].decode() not in temp_sub.keys():
            temp_sub[words[1].decode()] = words[1].decode()
            print("sub temp dictionary is: " , temp_sub)
            with open('register.txt', 'a') as f:
                f.write(message.decode()+"\n")
    elif words[0].decode() == "sub_humidity":
        if words[1].decode() not in humd_sub.keys():
            humd_sub[words[1].decode()] = words[1].decode()
            print("sub humidity dictionary is: " , humd_sub)
            with open('register.txt', 'a') as f:
                f.write(message.decode()+"\n")






    time.sleep(1)


    socket.send(b"registered")


