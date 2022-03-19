import netifaces
import argparse
import logging
import zmq
import csv
import time
import threading
from kademlia.network import Server
import asyncio

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
            print("Trying to reach", address)
            connect_str = "tcp://" + address

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
        events = dict(self.poller.poll(1000))
        for i in range(len(self.addresses)):
            print("event begin")
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
            print("completed one event")

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

    args = parser.parse_args()
    return args




class KademliaClient:
    # Initialize with an integer port and a list of
    # string,int pairs indicating the hosts to bootstrap against.
    # for example:
    # kad_client = KademliaClient(4321, [("10.0.0.1",4001), ("10.0.0.2",4001), ("10.0.0.2", 4002)]
    #
    # then use get or set to store and query data:
    # kad_client.set("foo", "bar")
    # print(kad_client.get("foo"))
    #
    # If you create additional threads to interact with this client,
    # aside from the main thread that your program runs on,
    # make sure each additional thread has an event loop by doing something
    # like this at the beginning of the thread:
    # event_loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(event_loop)
    #
    def __init__(self, kademlia_port, kademlia_hosts):
        self.kademlia_hosts = kademlia_hosts
        self.kademlia_port = kademlia_port
        self.kademlia_node = None

        # Create a lock for serializing get/set
        self.kad_lock = threading.Lock()

        # Initialize the event loop variable for the Kademlia server
        self.kad_loop = None

        # Get the current event loop
        loop = asyncio.get_event_loop()

        # Create a future to signal when Kademlia has been initialized
        self.start_future = loop.create_future()

        # Create a thread for running the kademlia event loop
        kthread = threading.Thread(group=None, target=self.kad_background_loop)

        # Start the kademlia thread
        kthread.start()

        # Wait for Kademlia to be initialized
        loop.run_until_complete(self.start_future)

    # Performs a get against the Kademlia node, storing the result in the
    # resp_future parameter
    async def do_get(self, name, resp_future):
        # Perform the get
        result = await self.kademlia_node.get(name)

        # Store the result in the future, using the future's own event loop
        resp_future.get_loop().call_soon_threadsafe(resp_future.set_result, result)

    # performs a set against the Kademlia node, storing True in the resp_future
    # parameter to indicate success
    async def do_set(self, name, value, resp_future):
        # Perform the set
        await self.kademlia_node.set(name, value)

        # Store True in the resp_future to signal completion
        resp_future.get_loop().call_soon_threadsafe(resp_future.set_result, True)

    def kad_background_loop(self):
        try:
            # Create a new event loop
            self.kad_loop = asyncio.new_event_loop()

            # Make it the event loop for this thread
            asyncio.set_event_loop(self.kad_loop)

            # Initialized the Kademlia node
            self.kad_loop.run_until_complete(self.init_server())

            # Signal that Kademlia has been initialized
            self.start_future.get_loop().call_soon_threadsafe(self.start_future.set_result, True)

            # Run the kademlia event loop forever
            # This allows the Kademlia node to process requests in the background
            self.kad_loop.run_forever()
        except Exception as e:
            print(e, flush=True)

    # Performs a Kademlia get
    def get(self, name):
        # Lock to make sure there is only one pending get or set
        self.kad_lock.acquire()
        try:
            # Get the current event loop
            loop = asyncio.get_event_loop()

            # Create a future from the current event loop
            resp_future = loop.create_future()

            # Call do_get using the existing Kademlia event loop
            self.kad_loop.call_soon_threadsafe(asyncio.ensure_future, self.do_get(name, resp_future))

            # Wait for the result to be stored in resp_future and then return it
            return loop.run_until_complete(resp_future)
        finally:
            # Release the lock when finished
            self.kad_lock.release()

    def set(self, name, value):
        # Lock to make sure there is only one pending get or set
        self.kad_lock.acquire()
        try:
            # Get the current event loop
            loop = asyncio.get_event_loop()

            # Create a future from the current event loop
            resp_future = loop.create_future()

            # Call do_set using the existing Kademlia event loop
            self.kad_loop.call_soon_threadsafe(asyncio.ensure_future, self.do_set(name, value, resp_future))

            # Wait for a result to be stored in resp_future
            # indicating that the set is complete
            loop.run_until_complete(resp_future)
            return
        finally:
            # Release the lock when finished
            self.kad_lock.release()

    async def init_server(self):
        try:
            # Create a Kademlia node
            self.kademlia_node = Server()

            # Set the port that the node listens on
            await self.kademlia_node.listen(self.kademlia_port)

            # Provide a list of Kademlia hosts to bootstrap against
            await self.kademlia_node.bootstrap(self.kademlia_hosts)
        except Exception as e:
            print(e, flush=True)
