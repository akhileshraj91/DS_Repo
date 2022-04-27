
import sys

import argparse

from kazoo.client import KazooClient   # client API
from kazoo.client import KazooState    # for the state machine

import logging
logging.basicConfig ()

def listener4state (state):
    if state == KazooState.LOST:
        print ("Current state is now = LOST")
    elif state == KazooState.SUSPENDED:
        print ("Current state is now = SUSPENDED")
    elif state == KazooState.CONNECTED:
        print ("Current state is now = CONNECTED")
    else:
        print ("Current state now = UNKNOWN !! Cannot happen")
        

class ZK_Driver ():

    def __init__ (self, args):
        self.zk = None  # session handle to the zookeeper server
        self.zkIPAddr = args.zkIPAddr  # ZK server IP address
        self.zkPort = args.zkPort # ZK server port num
        self.zkName = args.zkName # refers to the znode path being manipulated
        self.zkVal = args.zkVal # refers to the znode value



    def dump (self):
        """dump contents"""
        print ("=================================")
        print ("Server IP: {}, Port: {}; Path = {} and Val = {}".format (self.zkIPAddr, self.zkPort, self.zkName, self.zkVal))
        print ("=================================")

    def init_driver (self):
        """Initialize the client driver program"""

        try:
            self.dump ()

            hosts = self.zkIPAddr + str (":") + str (self.zkPort)
            print ("Driver::init_driver -- instantiate zk obj: hosts = {}".format(hosts))

            self.zk = KazooClient (hosts)

            self.zk.add_listener (listener4state)
            print ("Driver::init_driver -- state after connect = {}".format (self.zk.state))
            
        except:
            print ("Unexpected error in init_driver:", sys.exc_info()[0])
            raise



    def watch_znode_data_change (self):


        @self.zk.DataWatch(self.zkName)
        def dump_data_change (data, stat):
            print ("\n*********** Inside watch_znode_data_change *********")
            print(("Data changed for znode: data = {}, stat = {}".format (data,stat)))
            print ("*********** Leaving watch_znode_data_change *********")

    


    def start_session (self):
        """ Starting a Session """
        try:
            self.zk.start ()

        except:
            print("Exception thrown in start (): ", sys.exc_info()[0])
            return


    def stop_session (self):
        """ Stopping a Session """
        try:

            self.zk.stop ()

        except:
            print("Exception thrown in stop (): ", sys.exc_info()[0])
            return


    def create_znode (self):
        """ ******************* znode creation ************************ """
        try:

            print ("Creating an ephemeral znode {} with value {}".format(self.zkName,self.zkVal))
            self.zk.create (self.zkName, value=self.zkVal, ephemeral=True, makepath=True)

        except:
            print("Exception thrown in create (): ", sys.exc_info()[0])
            return


    def get_znode_value (self):
        
        """ ******************* retrieve a znode value  ************************ """
        try:

            print ("Checking if {} exists (it better be)".format(self.zkName))
            if self.zk.exists (self.zkName):
                print ("{} znode indeed exists; get value".format(self.zkName))


                value,stat = self.zk.get (self.zkName)
                print(("Details of znode {}: value = {}, stat = {}".format (self.zkName, value, stat)))

            else:
                print ("{} znode does not exist, why?".format(self.zkName))

        except:
            print("Exception thrown checking for exists/get: ", sys.exc_info()[0])
            return


    def modify_znode_value (self, new_val):
        
        """ ******************* modify a znode value  ************************ """
        try:

            print ("Setting a new value = {} on znode {}".format (new_val, self.zkName))

            if self.zk.exists (self.zkName):
                print ("{} znode still exists :-)".format(self.zkName))

                print ("Setting a new value on znode")
                self.zk.set (self.zkName, new_val)

                value,stat = self.zk.get (self.zkName)
                print(("New value at znode {}: value = {}, stat = {}".format (self.zkName, value, stat)))

            else:
                print ("{} znode does not exist, why?".format(self.zkName))

        except:
            print("Exception thrown checking for exists/set: ", sys.exc_info()[0])
            return


    def run_driver (self):
        """The actual logic of the driver program """
        try:

            print ("\n")
            input ("Starting Session with the ZooKeeper Server -- Press any key to continue")
            self.start_session ()
 
            print ("\n")
            input ("Creating a znode -- Press any key to continue:")
            self.create_znode ()

            print ("\n")
            input ("Obtain stored value -- Press any key to continue")
            self.get_znode_value ()

            print ("\n")
            input ("Modify stored value -- Press any key to continue")
            self.modify_znode_value (b"bar2")

            print ("\n")
            input ("Obtain the modified stored value -- Press any key to continue")
            self.get_znode_value ()

            print ("\n")
            input ("Disconnect from the server -- Press any key to continue")
            self.stop_session ()

            print ("\n")
            input ("Starting new Session to the ZooKeeper Server -- Press any key to continue")
            self.start_session ()
 
            print ("\n")
            input ("check if the node still exists -- Press any key to continue")
            if self.zk.exists (self.zkName):
                print ("{} znode still exists -- not possible".format (self.zkName))
            else:
                print ("{} znode no longer exists as expected".format (self.zkName))

            print ("\n")
            input ("Disconnecting for the final time -- Press any key to continue")
            self.stop_session ()

            print ("\n")
            input ("Cleaning up the handle -- Press any key to continue")
            self.zk.close ()

        except:
            print("Exception thrown: ", sys.exc_info()[0])



def parseCmdLineArgs ():
    parser = argparse.ArgumentParser ()

    parser.add_argument ("-a", "--zkIPAddr", default="127.0.0.1", help="ZooKeeper server ip address, default 127.0.0.1")
    parser.add_argument ("-p", "--zkPort", type=int, default=2181, help="ZooKeeper server port, default 2181")
    parser.add_argument ("-n", "--zkName", default="/foo", help="ZooKeeper znode name, default /foo")
    parser.add_argument ("-v", "--zkVal", default=b"bar", help="ZooKeeper znode value at that node, default 'bar'")
    
    args = parser.parse_args ()

    return args
    

def main ():
    """ Main program """

    print ("Demo program for ZooKeeper")
    parsed_args = parseCmdLineArgs ()
    

    driver = ZK_Driver (parsed_args)

    driver.init_driver ()
    
    driver.run_driver ()

if __name__ == '__main__':
    main ()
