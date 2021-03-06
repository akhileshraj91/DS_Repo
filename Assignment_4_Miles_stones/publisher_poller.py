
import sys
import time
import zmq
from random import randrange
import useful_fns
import json
import random
import keyboard
from collections import deque
args = useful_fns.parseCmdLineArgs()

def zk_main ():

    print("Registering the publisher with zookeeper")
    parsed_args = useful_fns.parseCmdLineArgs ()
    

    client = useful_fns.ZK_ClientApp (parsed_args)

    client.init_client ()
    
    client.run_client ()
    value = None
    flag =0

    while value == None:   
        time.sleep(1)
        zipcodes = client.zk.get_children ("/MAIN/leader_pub")
        # print(zipcodes)
        if zipcodes != []:
            zipcodes = zipcodes[0]
            # print(zipcodes,args.zipcode)
            name,_ = client.zk.get ("/MAIN/leader_pub/"+zipcodes)
            # print(name,args.name)

            name = name.decode()
            # print(name,args.name)
            if name == args.name and zipcodes == args.zipcode:

                value, stat = client.zk.get ("/MAIN/leaders/register")

                print(value.decode())
                client.zk.delete ("/MAIN/leader_pub/"+zipcodes,recursive=True)

                return value.decode()
            else:
                continue


srv_addr = zk_main()

zip_code = args.zipcode

IP = useful_fns.get_default_addr()
PORT = randrange(5000,9999)
PORT = str(PORT)


context = zmq.Context()
socket_register = context.socket(zmq.REQ)
# srv_addr = "10.0.0.1"
connect_str = "tcp://" + srv_addr + ":5555"
socket_register.connect (connect_str)
kind = "PUB"
while True:
    string_send = str(kind + " " + IP + ":" + PORT + " " + zip_code)
    print(string_send)
    socket_register.send(string_send.encode())
    print("Attempting to register the device")

    message = socket_register.recv().decode()
    cm = message.split()
    if cm[0] == "registered":
        print(cm[0])
        break



bind_str = "tcp://*:"+PORT

socket = context.socket (zmq.PUB)
socket.bind (bind_str)

params = args.info.split(",")
print(params)
start_time = time.time()
data_history = deque([])
flag = 0
while True:
    para = random.choice(params)
    if para == "temp":  # temp
        temp = randrange (-10, 101)
        topic = "temp:" + " " + zip_code + " " + str (temp)+ " " + str(time.time()) 
    elif para == "humidity": # humidity
        humidity = randrange (20, 101)
        topic = "humidity:" + " " + zip_code + " " + str (humidity)+ " "+ str(time.time())
    elif para == "pressure": # pressure
        pressure = randrange (26, 34)
        topic = "pressure:" + " " + zip_code + " " + str (pressure)+ " " + str(time.time())
    else:
        print ("bad category")
        continue
    if len(data_history) <= 5:    
        data_history.append(topic)
    else:
        data_history.popleft()
        data_history.append(topic)
    # print(data_history)
    print ("Sending: {}".format (topic))
    socket.send_string (topic)
    time.sleep (1)  

    if time.time()-start_time > args.duration:
        while True:
            string_send = str("remove" + " " + IP + ":" + PORT + " " + zip_code)
            print(string_send)
            socket_register.send(string_send.encode())
            message = socket_register.recv().decode()
            cm = message.split()
            if cm[0] == "removed":
                print(cm[0])
                break

        break
