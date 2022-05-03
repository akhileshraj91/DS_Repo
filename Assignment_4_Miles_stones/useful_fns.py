import netifaces
import argparse
import logging
import zmq
import csv
import time
import threading
from kademlia.network import Server
import asyncio
import os
import sys
import time

import argparse
import random

from kazoo.client import KazooClient

import logging


from kademlia_dht import Kademlia_DHT

import logging
logging.basicConfig ()



class ZK_ClientApp ():
    def __init__ (self, args):
        self.IP = get_default_addr()
        self.zipcode = args.zipcode
        self.name = args.name
        self.zkIPAddr = args.zkIPAddr  
        self.zkPort = args.zkPort 
        self.ppath = "/MAIN"
        self.registerpath = "/MAIN/register"
        self.brokerpath = "/MAIN/broker" 
        self.bleaderpath = "/MAIN/leaders"
        self.PUBS = args.users
        self.zk = None  
        self.flag = False 

    def init_client (self):

        try:
            print(("ClientApp::run - Client {} now running and opening connection to zookeeper".format (self.name)))


            hosts = self.zkIPAddr + str (":") + str (self.zkPort)
            self.zk = KazooClient (hosts)
            print(("ClientApp::run -- state = {}".format (self.zk.state)))

        except:
            print("Unexpected error in ClientApp::run", sys.exc_info()[0])
            raise

    def run_client (self):
        try:
            self.zk.start()
            while (True):
                # print(self.ppath)
                if self.zk.exists (self.ppath):
                    if "register" in self.name:
                        self.zk.create (self.registerpath+"/"+self.name,value=self.IP.encode(), ephemeral=True)
                        self.zk.set (self.ppath+"/"+"leaders"+"/"+ "register",value=self.IP.encode())

                    elif "broker" in self.name:
                        # print("THIS IS A BROKER")
                        self.zk.create (self.brokerpath+"/"+self.name,value=self.IP.encode(),ephemeral=True)
                        self.zk.create (self.ppath+"/"+"active_brokers"+"/"+self.name,value=self.IP.encode(),ephemeral=True)
                        if self.zk.get_children (self.ppath+"/"+"leaders"+"/"+ "broker") != []:
                            # print("NODE EXISTS")
                            # value,data = self.zk.get(self.ppath+"/"+"leaders"+"/"+ "broker"+"/"+self.name,value=self.IP.encode(),ephemeral=True)
                            bro_count,_ = self.zk.get(self.brokerpath) 
                            # print("___________________",bro_count.decode())
                            bc = bro_count.decode()
                            new_count = str(int(bc) + 1)

                            self.zk.set (self.brokerpath,value=new_count.encode())

                        # if value.decode() == '0':
                        else:
                            # print("WHY IS THIS NOT GETTING CHOSEN")
                            # self.zk.delete (self.bleaderpath+"/"+"broker",recursive=True)
                            self.zk.create (self.bleaderpath+"/"+"broker"+"/"+self.name,value=self.IP.encode(),ephemeral=True)
                            print("Leader chosen for the first time....................")


                    else:
                        # print("This is printing", self.name)
                        self.zk.create (self.ppath + str ("/") + self.name, value=self.IP.encode(),ephemeral=True)
                        if "register" in self.name:
                            self.zk.set (self.registerpath+"/"+ self.name,value=self.IP.encode())
                        if "broker" in self.name:
                            self.zk.set (self.brokerpath+"/"+self.name,value=self.IP.encode())

                        if "sub" in self.name:
                            cur_broker = self.zk.get_children(self.bleaderpath+"/"+"broker")
                            print(cur_broker)
                            broker_name = cur_broker[0]
                            self.zk.create (self.ppath+"/"+"subscribers"+"/"+self.name,value=broker_name.encode(),ephemeral=True)
                            sub_count,_ = self.zk.get(self.ppath+"/"+"subscribers")
                            sc = sub_count.decode() 
                            new_sc = str(int(sc)+1)
                            # print("""""""""""""""""""""""""""""""""""",new_sc)
                            self.zk.set (self.ppath+"/"+"subscribers",value=new_sc.encode())
                    break


                else:
                    print(("ClientApp::run {} - parent znode is set".format (self.name)))
                    self.zk.start ()
                    self.zk.create (self.ppath,value=b'0')
                    self.zk.create (self.brokerpath,value=b'0')
                    self.zk.create (self.registerpath,value=b'0')
                    self.zk.create (self.bleaderpath,value=b'0')
                    self.zk.create (self.bleaderpath+"/"+"broker",value=b'0')
                    self.zk.create (self.bleaderpath+"/"+ "register",ephemeral=True)
                    self.zk.create (self.ppath+"/"+"subscribers",value=b'0')
                    self.zk.create (self.ppath+"/"+"active_brokers",value=b'0')
                    self.zk.create (self.ppath+"/"+"BS_data",value=b'0')

                    # time.sleep(1)





            if "broker" in self.name:
                @self.zk.ChildrenWatch (self.bleaderpath+"/"+"broker") 
                def child_change_watcher (children):

                    print(("Driver::run -- children watcher: num childs = {}".format (len (children))))
                    print("Triggered the watcher")

                    if self.zk.get_children (self.ppath+"/"+"leaders"+"/"+ "broker") != []:
                        print("path exists")  

                    else:
                        self.zk.delete (self.bleaderpath+"/"+"broker",recursive=True) 
                        self.zk.create (self.bleaderpath+"/"+"broker",value=b'0')
                        try:
                            self.zk.create (self.bleaderpath+"/"+"broker"+"/"+self.name,value=self.IP.encode(),ephemeral=True)
                            print("Leader reinitialized..............................................")
                        except:
                            # print("Unexpected error in ClientApp::run", sys.exc_info()[0])
                            pass
                            # value,data = self.zk.get(self.bleaderpath+"/"+"broker")
                            # print(value,data)



                # @self.zk.DataWatch (self.brokerpath)
                # def data_change_watcher (data, stat):
                #     """Data Change Watcher"""
                #     print(("ClientApp::DataChangeWatcher {} - data = {}, stat = {}".format (self.name, data, stat)))
                #     value = int (data)
                #     print(value)
                #     # if (value == self.cond):
                #     #     print(("ClientApp: {}, barrier is reached".format (self.name)))
                #     #     self.barrier = True


            if "register" in self.name:
                @self.zk.DataWatch (self.ppath+"/"+"subscribers")
                def data_change_watcher (data, stat):
                    """Data Change Watcher"""
                    print(("ClientApp::DataChangeWatcher {} - data = {}, stat = {}".format (self.name, data, stat)))
                    value = int (data)
                    print(value)

                    if value >= 2:
                        while True:
                            available_brokers = self.zk.get_children(self.brokerpath)
                            new_leader = random.choice(available_brokers)
                            print("________________________",new_leader)

                            new_ip,_ = self.zk.get(self.brokerpath+"/"+new_leader)
                            print(new_ip)
                            self.zk.delete (self.brokerpath+"/"+new_leader,recursive=True)

                            # print("_______________________",new_ip.decode())
                            new_val = new_ip.decode()
                            old_val= self.zk.get_children(self.bleaderpath+"/"+"broker")
                            value = str(value)
                            self.zk.create (self.ppath+"/"+"BS_data"+"/"+old_val[0],value=value.encode())
                            # old_val = old_val.decode()
                            print("___",old_val[0])
                            if new_leader != old_val[0]:
                                self.zk.delete (self.bleaderpath+"/"+"broker",recursive=True)
                                self.zk.create (self.bleaderpath+"/"+"broker",value=b'0')
                                self.zk.create (self.bleaderpath+"/"+"broker"+"/"+new_leader,value=new_val.encode(),ephemeral=True)
                                if self.zk.exists (self.ppath+"/"+"BS_data"+"/"+new_leader):
                                    self.zk.set (self.ppath+"/"+"subscribers",value=b'0')

                                else:
                                    n_val,_ = self.zk.get(self.ppath+"/"+"BS_data"+"/"+new_leader)
                                    print("NEW BROKER DETAILS UPDATED")
                                    self.zk.set (self.ppath+"/"+"subscribers",value=n_val)
                                break
                            else:
                                continue
                        print("new broker is:", new_leader , "and IP is:", new_ip)


                @self.zk.ChildrenWatch (self.ppath+"/"+"subscribers") 
                def child_change_watcher (children):
                    print(("Driver::run -- children watcher: num childs = {}".format (len (children))))
                    print("Triggered the watcher")
                    print(children)
                    self.zk.getACL(self.ppath+"/"+"subscribers")

                    # if self.zk.exists (self.ppath+"/"+"BS_data"):
                    #     print("path exists")  

                    # else:
                    #     try:
                    #         self.zk.create (self.bleaderpath+"/"+"broker",value=self.IP.encode(),ephemeral=True)
                    #         print("Leader reinitialized..............................................")
                    #     except:
                    #         # print("Unexpected error in ClientApp::run", sys.exc_info()[0])
                    #         pass


    
        except:
            print("Unexpected error in ClientApp::run", sys.exc_info()[0])
            # raise
            pass


def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    # print("^^^^^^^^^^^^^^^^^^^",dict1,"!!",dict2,"##",res)
    return res

def get_default_addr():
    for interface in netifaces.interfaces():
        # Skip loopback interface for now
        if interface.startswith("lo"):
            continue

        addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addrs and len(addrs[netifaces.AF_INET]) > 0:
            return addrs[netifaces.AF_INET][0]["addr"]
    return "127.0.0.1"


class CS6381_Subscriber():

    def __init__(self, args):
        self.zip_code = args.zipcode
        self.params = args.info.split(",")
        self.context = None

        self.poller = None

        self.temp_socket = []
        self.pressure_socket = []
        self.humidity_socket = []
        self.addresses = []
        self.subscribers = []
        self.name = None
        self.broker_in_use = 0

    def configure(self, strat="direct"):
        self.name = self.zip_code + strat

        self.context = zmq.Context()

        self.poller = zmq.Poller()

        if strat == "indirect broker":
            self.zip_code = ""

        for i in range(len(self.addresses)):
            address = self.addresses[i]
            # print("Trying to reach", address)
            connect_str = "tcp://" + address
            # print("reached")
            # print(self.params)
            # print(connect_str)

            if "temp" in self.params:
                self.temp_socket.append(self.context.socket(zmq.SUB))
                self.temp_socket[i].connect(connect_str)
                filter = "temp:" + " " + self.zip_code
                # print(filter)
                self.temp_socket[i].setsockopt_string(zmq.SUBSCRIBE, filter)
                self.poller.register(self.temp_socket[i], zmq.POLLIN)
            if "humidity" in self.params:
                self.humidity_socket.append(self.context.socket(zmq.SUB))
                self.humidity_socket[i].connect(connect_str)
                filter = "humidity:" + " " + self.zip_code
                # print(filter)
                self.humidity_socket[i].setsockopt_string(zmq.SUBSCRIBE, filter)
                self.poller.register(self.humidity_socket[i], zmq.POLLIN)
            if "pressure" in self.params:
                self.pressure_socket.append(self.context.socket(zmq.SUB))
                self.pressure_socket[i].connect(connect_str)
                filter = "pressure:" + " " + self.zip_code
                # print(filter)
                self.pressure_socket[i].setsockopt_string(zmq.SUBSCRIBE, filter)
                self.poller.register(self.pressure_socket[i], zmq.POLLIN)


    def event_loop(self):
        # while True:
        events = dict(self.poller.poll(5000))
        for i in range(len(self.addresses)):
            # print("event begin")
            if "temp" in self.params and self.temp_socket[i] in events:
                string = self.temp_socket[i].recv_string()
                print("Subscriber:recv_temp, value = {}".format(string))
                sent_time = string.split()[-1]
                recv_time = time.time()
                transmission_time = recv_time - float(sent_time)
                with open("./logs/%s_trans.csv" % (self.name), 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([sent_time, recv_time, transmission_time])

            if "humidity" in self.params and self.humidity_socket[i] in events:
                string = self.humidity_socket[i].recv_string()
                print("Subscriber:recv_humidity, value = {}".format(string))
                sent_time = string.split()[-1]
                recv_time = time.time()
                transmission_time = recv_time - float(sent_time)
                with open("./logs/%s_trans.csv" % (self.name), 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([sent_time, recv_time, transmission_time])

            if "pressure" in self.params and self.pressure_socket[i] in events:
                string = self.pressure_socket[i].recv_string()
                print("Subscriber:recv_pressure, value = {}".format(string))
                sent_time = string.split()[-1]
                recv_time = time.time()
                transmission_time = recv_time - float(sent_time)
                with open("./logs/%s_trans.csv" % (self.name), 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([sent_time, recv_time, transmission_time])
            # print("completed one event")


        self.context = None
        self.poller = None
        self.temp_socket = []
        self.pressure_socket = []
        self.humidity_socket = []
        self.addresses = []


    def broker_loop(self, PORT):
        if not self.broker_in_use:
            self.socket_broker = self.context.socket(zmq.PUB)
            self.socket_broker.bind("tcp://*:" + PORT)
            self.broker_in_use = 1
        # while True:
        events = dict(self.poller.poll(1000))
        for i in range(len(self.addresses)):
            if "temp" in self.params and self.temp_socket[i] in events:
                string = self.temp_socket[i].recv_string()
                # print("Subscriber:recv_temp, value = {}".format(string))
                self.socket_broker.send_string(string)

            if "humidity" in self.params and self.humidity_socket[i] in events:
                string = self.humidity_socket[i].recv_string()
                # print("Subscriber:recv_humidity, value = {}".format(string))
                self.socket_broker.send_string(string)

            if "pressure" in self.params and self.pressure_socket[i] in events:
                string = self.pressure_socket[i].recv_string()
                # print("Subscriber:recv_pressure, value = {}".format(string))
                self.socket_broker.send_string(string)
        
        self.context = None
        self.poller = None
        self.temp_socket = []
        self.pressure_socket = []
        self.humidity_socket = []
        self.addresses = []
        

    def get_pubs(self, my_dict, strat="direct"):
        if strat == "indirect":
            for ele in my_dict:
                self.addresses.append(ele)
            # self.addresses.append(my_dict)
            # for key, value in my_dict.items():
            #     self.addresses.append(key)
        else:
            for ele in my_dict:
                self.addresses.append(ele)
            # self.addresses.append(my_dict)
            # for key, value in my_dict.items():
            #     if value == self.zip_code:
            #         self.addresses.append(key)

    def get_subs(self, my_dict, strat="direct"):
        if strat == "indirect":
            self.subscribers = my_dict.keys()

        else:
            for key, value in my_dict.items():
                if value == self.zip_code:
                    self.subscribers.append(key)


def parseCmdLineArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--strategy", default="direct", help="direct or indirect, default direct")
    parser.add_argument("-i", "--info", default="temp,humidity,pressure",
                        help="give the publishing information in order")
    parser.add_argument("-z", "--zipcode", default="37209", help="Enter a 5 digit zipcode")
    parser.add_argument("-d", "--debug", default=logging.WARNING, action="store_true",
                        help="Logging level (see logging package): default WARNING else DEBUG")
    parser.add_argument("-a", "--ipaddr", type=str, default=None, help="IP address of any existing DHT node")
    parser.add_argument("-p", "--port", help="port number used by one or more DHT nodes", type=int, default=8468)
    parser.add_argument("-o", "--override_port",
                        help="overriden port number used by our node. Used if we want to create many nodes on the same host",
                        type=int, default=None)
    parser.add_argument("-k", "--key", type=str, default=None, help="Key to set value under")
    parser.add_argument("-v", "--value", type=str, default=None, help="value for the key to set under")
    parser.add_argument("-t", "--duration", type=int, default=1000, help="duration of a publisher")


    parser.add_argument ("-zka", "--zkIPAddr", default="127.0.0.1", help="ZooKeeper server ip address, default 127.0.0.1")
    parser.add_argument ("-c", "--numClients", type=int, default=5, help="Number of client apps in the barrier, default 5")

    parser.add_argument ("-co", "--cond", type=int, default=5, help="Barrier Condition representing number of client apps in the barrier, default 5")

    parser.add_argument ("-zkp", "--zkPort", type=int, default=2181, help="ZooKeeper server port, default 2181")
    parser.add_argument ("-u", "--users", type=int, default=10, help="Number of users/subscribers allowed per broker")



    parser.add_argument ("name", default = "None", help="client name")

    args = parser.parse_args()
    return args




class KademliaClient:
    #
    def __init__(self, kademlia_port, kademlia_hosts):
        self.kademlia_hosts = kademlia_hosts
        self.kademlia_port = kademlia_port
        self.kademlia_node = None

        self.kad_lock = threading.Lock()

        self.kad_loop = None

        loop = asyncio.get_event_loop()

        self.start_future = loop.create_future()

        kthread = threading.Thread(group=None, target=self.kad_background_loop)

        kthread.start()

        loop.run_until_complete(self.start_future)


    async def do_get(self, name, resp_future):
        result = await self.kademlia_node.get(name)

        resp_future.get_loop().call_soon_threadsafe(resp_future.set_result, result)

    async def do_set(self, name, value, resp_future):
        await self.kademlia_node.set(name, value)

        resp_future.get_loop().call_soon_threadsafe(resp_future.set_result, True)

    def kad_background_loop(self):
        try:
            self.kad_loop = asyncio.new_event_loop()

            asyncio.set_event_loop(self.kad_loop)

            self.kad_loop.run_until_complete(self.init_server())

            self.start_future.get_loop().call_soon_threadsafe(self.start_future.set_result, True)

            self.kad_loop.run_forever()
        except Exception as e:
            print(e, flush=True)

    def get(self, name):
        self.kad_lock.acquire()
        try:
            loop = asyncio.get_event_loop()

            resp_future = loop.create_future()

            self.kad_loop.call_soon_threadsafe(asyncio.ensure_future, self.do_get(name, resp_future))

            return loop.run_until_complete(resp_future)
        finally:
            self.kad_lock.release()

    def set(self, name, value):
        self.kad_lock.acquire()
        try:
            loop = asyncio.get_event_loop()

            resp_future = loop.create_future()

            self.kad_loop.call_soon_threadsafe(asyncio.ensure_future, self.do_set(name, value, resp_future))

            loop.run_until_complete(resp_future)
            return
        finally:
            self.kad_lock.release()

    async def init_server(self):
        try:
            self.kademlia_node = Server()

            await self.kademlia_node.listen(self.kademlia_port)

            await self.kademlia_node.bootstrap(self.kademlia_hosts)
        except Exception as e:
            print(e, flush=True)




