import argparse   
import logging    
import useful_fns
import zmq
from kademlia_dht import Kademlia_DHT

def register_DHT():
    IP = useful_fns.get_default_addr()
    context = zmq.Context()
    socket_register = context.socket(zmq.REQ)
    srv_addr = "10.0.0.1"
    connect_str = "tcp://" + srv_addr + ":5555"
    socket_register.connect (connect_str)
    kind = "DHT"

    while True:
        string_send = str(kind + " " + IP + ":")
        socket_register.send(string_send.encode())
        print("Attempting to register the DHT server")
        message = socket_register.recv().decode()
        cm = message.split()
        if cm[0] == "registered":
            print(cm[0])
            break

def parseCmdLineArgs ():
    parser = argparse.ArgumentParser (description="Kademlia bootstrapping")
    parser.add_argument ("-c", "--create", default=False, action="store_true", help="Create a new DHT ring, otherwise we join a DHT") 
    parser.add_argument ("-d", "--debug", default=logging.WARNING, action="store_true", help="Logging level (see logging package): default WARNING else DEBUG")
    parser.add_argument ("-i", "--ipaddr", type=str, default=None, help="IP address of any existing DHT node")
    parser.add_argument ("-p", "--port", help="port number used by one or more DHT nodes", type=int, default=8468)
    parser.add_argument ("-o", "--override_port", help="overriden port number used by our node. Used if we want to create many nodes on the same host", type=int, default=None)

    return parser.parse_args()


def main ():
    print ("Main: parse command line arguments")
    args = parseCmdLineArgs ()
    register_DHT()
    print ("Main: Instantiate the Kademlia DHT object")
    if (args.create):
        kdht = Kademlia_DHT (True)
    else:
        kdht = Kademlia_DHT ()
        

    print ("Main: Initialize the Kademlia DHT object")
    if (not kdht.initialize (args)):
        print ("Main: Initialization of Kademlia DHT failed")
        return
    
    # check if this is the first node of the ring or others joining
    # an existing one
    if (args.create):
        print ("Main: create the first DHT node")
        kdht.create_bootstrap_node ()
    else:
        print ("Main: join some DHT node")
        kdht.connect_to_bootstrap_node ()


if __name__ == "__main__":
    main()
