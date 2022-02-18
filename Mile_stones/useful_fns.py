import netifaces
import argparse
import sys
import zmq

def get_default_addr():
    for interface in netifaces.interfaces():
        # Skip loopback interface for now
        if interface.startswith("lo"):
            continue

        addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addrs and len(addrs[netifaces.AF_INET]) > 0:
            return addrs[netifaces.AF_INET][0]["addr"]
    return "127.0.0.1"


def get_key(val,my_dict):
    adds = []
    for key, value in my_dict.items():
         if val == value:
             adds.append(key)
    return adds


class CS6381_Subscriber ():

    def __init__ (self, args):
        self.addr = args.addr   
        self.temp = args.temp 
        self.pressure = args.pressure 
        self.humidity = args.humidity 
        self.zip_code = args.zipcode
        
        self.context = None

        self.poller = None
        
        self.temp_socket = []
        self.pressure_socket = []
        self.humidity_socket = []

    def configure (self, address_list):
        self.context = zmq.Context()

        self.poller = zmq.Poller ()

        for i in range(len(address_list)):

            self.temp_socket.append(self.context.socket (zmq.SUB))
            self.humidity_socket.append(self.context.socket (zmq.SUB))
            self.pressure_socket.append(self.context.socket (zmq.SUB))
            address = address_list[i]
            connect_str = "tcp://" + address
            self.temp_socket[i].connect (connect_str)
            self.humidity_socket[i].connect (connect_str)
            self.pressure_socket[i].connect (connect_str)
        
            filter = "temp:" + self.zip_code
            self.temp_socket[i].setsockopt_string(zmq.SUBSCRIBE, filter)
            filter = "humidity:" + self.zip_code
            self.humidity_socket[i].setsockopt_string(zmq.SUBSCRIBE, filter)
            filter = "pressure:" + self.zip_code
            self.pressure_socket[i].setsockopt_string(zmq.SUBSCRIBE, filter)
            
            self.poller.register (self.temp_socket[i], zmq.POLLIN)
            self.poller.register (self.humidity_socket[i], zmq.POLLIN)
            self.poller.register (self.pressure_socket[i], zmq.POLLIN)


    def event_loop (self, address_list):
        while True:

            events = dict (self.poller.poll ())

            for i in range(len(address_list)):
                if self.temp_socket[i] in events:
                    string = self.temp_socket[i].recv_string()
                    print ("Subscriber:recv_temp, value = {}".format (string))
                
                if self.humidity_socket[i] in events:
                    string = self.humidity_socket[i].recv_string()
                    print ("Subscriber:recv_humidity, value = {}".format (string))
                
                if self.pressure_socket[i] in events:
                    string = self.pressure_socket[i].recv_string()
                    print ("Subscriber:recv_pressure, value = {}".format (string))


def parseCmdLineArgs ():
    parser = argparse.ArgumentParser ()
    parser.add_argument ("-a", "--addr", default="localhost", help="Publisher IP address, default localhost")
    parser.add_argument ("-t", "--temp", default="70", help="Temperature, default 70 F")
    parser.add_argument ("-p", "--pressure", default="30", help="Pressure, default 30")
    parser.add_argument ("-m", "--humidity", default="50", help="Humidity, default 50")
    parser.add_argument ("-s", "--strategy", default="indirect", help="direct or indirect, default direct")
    parser.add_argument ("-i", "--info", default="temp,pressure,humidity", help="give the publishing information in order")
    parser.add_argument ("-z", "--zipcode", default="37209", help="Enter a 5 digit zipcode")
    args = parser.parse_args ()

    return args




