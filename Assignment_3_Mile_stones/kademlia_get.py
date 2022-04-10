

import argparse   
import logging     
import asyncio     

from kademlia_dht import Kademlia_DHT


def parseCmdLineArgs ():
    parser = argparse.ArgumentParser (description="Kademlia set value")

    parser.add_argument ("-d", "--debug", default=logging.WARNING, action="store_true", help="Logging level (see logging package): default WARNING else DEBUG")
    parser.add_argument ("-i", "--ipaddr", type=str, default=None, help="IP address of any existing DHT node")
    parser.add_argument ("-p", "--port", help="port number used by one or more DHT nodes", type=int, default=8468)
    parser.add_argument ("-o", "--override_port", help="overriden port number used by our node. Used if we want to create many nodes on the same host", type=int, default=None)

    parser.add_argument ("key", type=str, help="Key to get the value under it")
    
    return parser.parse_args ()


async def main ():
    # first parse the arguments
    print ("Main: parse command line arguments")
    args = parseCmdLineArgs ()

    print ("Main: Instantiate the Kademlia DHT object")
    kdht = Kademlia_DHT ()

    print ("Main: Initialize the Kademlia DHT object")
    if (not kdht.initialize (args)):
        print ("Main: Initialization of Kademlia DHT failed")
        return
    
    print ("Main: Bootstrap and key value for key")
    result = await kdht.get_value (args.key)

    print ("Main: returned result for key = {} is {}".format (args.key, result))


if __name__ == "__main__":
    asyncio.run (main ())

