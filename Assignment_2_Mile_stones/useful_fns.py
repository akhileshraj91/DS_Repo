import netifaces
import argparse
import logging
import zmq
import csv
import time

from kademlia_dht import Kademlia_DHT


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

    def configure(self, strat="direct"):
        self.name = self.zip_code + strat

        self.context = zmq.Context()

        self.poller = zmq.Poller()

        if strat == "indirect broker":
            self.zip_code = ""

        for i in range(len(self.addresses)):
            address = self.addresses[i]
            print(address)
            connect_str = "tcp://" + address
            # print(self.params)
            print(connect_str)

            if "temp" in self.params:
                self.temp_socket.append(self.context.socket(zmq.SUB))
                self.temp_socket[i].connect(connect_str)
                filter = "temp:" + " " + self.zip_code
                print(filter)
                self.temp_socket[i].setsockopt_string(zmq.SUBSCRIBE, filter)
                self.poller.register(self.temp_socket[i], zmq.POLLIN)
            if "humidity" in self.params:
                self.humidity_socket.append(self.context.socket(zmq.SUB))
                self.humidity_socket[i].connect(connect_str)
                filter = "humidity:" + " " + self.zip_code
                print(filter)
                self.humidity_socket[i].setsockopt_string(zmq.SUBSCRIBE, filter)
                self.poller.register(self.humidity_socket[i], zmq.POLLIN)
            if "pressure" in self.params:
                self.pressure_socket.append(self.context.socket(zmq.SUB))
                self.pressure_socket[i].connect(connect_str)
                filter = "pressure:" + " " + self.zip_code
                print(filter)
                self.pressure_socket[i].setsockopt_string(zmq.SUBSCRIBE, filter)
                self.poller.register(self.pressure_socket[i], zmq.POLLIN)

    def event_loop(self):
        while True:
            events = dict(self.poller.poll())
            for i in range(len(self.addresses)):
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

    def broker_loop(self, PORT):
        self.socket_broker = self.context.socket(zmq.PUB)
        self.socket_broker.bind("tcp://*:" + PORT)
        while True:
            events = dict(self.poller.poll())
            for i in range(len(self.addresses)):
                if "temp" in self.params and self.temp_socket[i] in events:
                    string = self.temp_socket[i].recv_string()
                    print("Subscriber:recv_temp, value = {}".format(string))
                    self.socket_broker.send_string(string)

                if "humidity" in self.params and self.humidity_socket[i] in events:
                    string = self.humidity_socket[i].recv_string()
                    print("Subscriber:recv_humidity, value = {}".format(string))
                    self.socket_broker.send_string(string)

                if "pressure" in self.params and self.pressure_socket[i] in events:
                    string = self.pressure_socket[i].recv_string()
                    print("Subscriber:recv_pressure, value = {}".format(string))
                    self.socket_broker.send_string(string)

    def get_pubs(self, my_dict, strat="direct"):
        if strat == "indirect":
            for key, value in my_dict.items():
                self.addresses.append(key)
        else:
            for key, value in my_dict.items():
                if value == self.zip_code:
                    self.addresses.append(key)

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
    args = parser.parse_args()
    return args


async def set_main(key, value):
    print("Main: Instantiate the Kademlia DHT object")
    kdht = Kademlia_DHT()

    print("Main: Initialize the Kademlia DHT object")
    if not key:
        print("Main: Initialization of Kademlia DHT failed")
        return

    print("Main: Bootstrap and set key-val")
    await kdht.set_value(key, value)


async def get_main(key):

    print("Main: Instantiate the Kademlia DHT object")
    kdht = Kademlia_DHT()

    print("Main: Initialize the Kademlia DHT object")
    if not key:
        print("Main: Initialization of Kademlia DHT failed")
        return

    print("Main: Bootstrap and key value for key")
    result = await kdht.get_value(key)

    print("Main: returned result for key = {} is {}".format(key, result))
