
import logging     
import asyncio     
from kademlia.network import Server  
class Kademlia_DHT ():

    def __init__ (self, create=False):
        self.create = create 
        self.server = None 
        self.logger = logging.getLogger ('kademlia') 
        self.my_port = None  
        self.bootstrap_ipaddr = None 
        self.bootstrap_port = None  

    def initialize (self, args):
        if (not self.create and args.ipaddr is None):
            print ("Kademlia_DHT::initialize - IP address for bootstrap node is not provided. Giving up")
            return False

        self.bootstrap_ipaddr = args.ipaddr
        
        if (args.override_port is None):
            self.bootstrap_port = args.port
            self.my_port = args.port
        else:
            self.bootstrap_port = args.port
            self.my_port = args.override_port

        print ("Kademlia_DHT::initialize - My port = {}, Bootstrap port = {}, Bootstrap IP Addr = {}".format (self.my_port, self.bootstrap_port, self.bootstrap_ipaddr))
        
        self.server = Server ()

        handler = logging.StreamHandler () 
        formatter = logging.Formatter ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter (formatter)
        self.logger.addHandler (handler)
        self.logger.setLevel (args.debug)

        return True

    def connect_to_bootstrap_node (self):
        loop = asyncio.get_event_loop ()
        loop.set_debug (True)

        loop.run_until_complete (self.server.listen (self.my_port))
        bootstrap_node = (self.bootstrap_ipaddr, int (self.bootstrap_port))
        loop.run_until_complete (self.server.bootstrap ([bootstrap_node]))

        try:
            loop.run_forever ()
        except KeyboardInterrupt:
            pass
        finally:
            self.server.stop ()
            loop.close ()


    def create_bootstrap_node (self):
        loop = asyncio.get_event_loop ()
        loop.set_debug (True)

        loop.run_until_complete (self.server.listen (self.my_port))

        try:
            loop.run_forever ()
        except KeyboardInterrupt:
            pass
        finally:
            self.server.stop ()
            loop.close ()

    async def set_value (self, key, value):
        await self.server.listen (self.my_port)
        bootstrap_node = (self.bootstrap_ipaddr, int (self.bootstrap_port))
        await self.server.bootstrap ([bootstrap_node])
        await self.server.set (key, value)
        self.server.stop ()

    async def get_value (self, key):
        await self.server.listen (self.my_port)
        bootstrap_node = (self.bootstrap_ipaddr, int (self.bootstrap_port))
        await self.server.bootstrap ([bootstrap_node])
        result = await self.server.get (key)
        self.server.stop ()
        return result

