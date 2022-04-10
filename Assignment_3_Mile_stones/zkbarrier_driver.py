
import os
import sys
import time

import argparse


from kazoo.client import KazooClient


import logging
logging.basicConfig ()


class ZK_Driver ():
    """ The ZooKeeper Driver Class """


    def __init__ (self, args):
        self.zkIPAddr = args.zkIPAddr  # ZK server IP address
        self.zkPort = args.zkPort # ZK server port num
        self.numClients = args.numClients # used as barrier condition
        self.zk = None  # session handle to the server
        self.path = "/barrier" # refers to the znode path being manipulated
        self.barrier = False



    def dump (self):
        """dump contents"""
        print ("=================================")
        print(("Server IP: {}, Port: {}; Path = {}, NumClients = {}".format (self.zkIPAddr, self.zkPort, self.path, self.numClients)))
        print ("=================================")


    def init_driver (self):
        """Initialize the client driver program"""

        try:
            self.dump ()


            hosts = self.zkIPAddr + str (":") + str (self.zkPort)
            print(("Driver::init_driver -- instantiate zk obj: hosts = {}".format(hosts)))
            self.zk = KazooClient (hosts)
            print(("Driver::init_driver -- state = {}".format (self.zk.state)))
            
        except:
            print("Unexpected error in init_driver:", sys.exc_info()[0])
            raise

    

    def run_driver (self):
        """The actual logic of the driver program """


        # first connect to the zookeeper server
        print ("Driver::run_driver -- connect with server")
        self.zk.start ()
        print(("Driver::run_driver -- state = {}".format (self.zk.state)))

        # next, create a znode for the barrier sync with initial value 0
        print ("Driver::run_driver -- create a znode for barrier")
        self.zk.create (self.path, value=b"0")


        @self.zk.ChildrenWatch (self.path)
        def child_change_watcher (children):
            """Children Watcher"""
            print(("Driver::run -- children watcher: num childs = {}".format (len (children))))


            if self.zk.exists (self.path):


                if (len (children) > 0):
                    print(("Driver::child_change_watcher - setting new value for children = {}".format (len(children))))
                    self.zk.set (self.path, str (len (children)).encode ())

                # has the number of children reached the barrier condition?
                if (self.numClients == len (children)):
                    self.barrier = True

            else:
                print ("Driver:run_driver -- child watcher -- znode does not exist")
        #-----------------------------------------------------------

        print ("Driver::run_driver -- wait for the clients to reach barrier")

        while (self.barrier == False):
            time.sleep (1)
            

        print ("Driver::run_driver -- now wait for clients to remove their znodes")
        while (True):
            # here we are sure our node exists
            value, stat = self.zk.get (self.path)
            if (stat.children_count == 0):
                # all child znodes are gone so get out of the loop
                print ("Driver::run_driver -- all client znodes are gone")
                break
                
        print(("Driver::run_driver -- now remove the znode {}".format (self.path)))
        self.zk.delete (self.path, recursive=True)
        
        print ("Driver::run_driver -- disconnect and close")
        self.zk.stop ()
        self.zk.close ()

        print ("Driver::run_driver -- Bye Bye")

def parseCmdLineArgs ():
    parser = argparse.ArgumentParser ()

    parser.add_argument ("-a", "--zkIPAddr", default="127.0.0.1", help="ZooKeeper server ip address, default 127.0.0.1")
    parser.add_argument ("-c", "--numClients", type=int, default=5, help="Number of client apps in the barrier, default 5")
    parser.add_argument ("-p", "--zkPort", type=int, default=2181, help="ZooKeeper server port, default 2181")
    

    args = parser.parse_args ()

    return args
    

def main ():
    """ Main program """

    print("Demo program for ZooKeeper-based Barrier Sync")
    parsed_args = parseCmdLineArgs ()
    
    driver = ZK_Driver (parsed_args)

    driver.init_driver ()
    
    driver.run_driver ()

if __name__ == '__main__':
    main ()
