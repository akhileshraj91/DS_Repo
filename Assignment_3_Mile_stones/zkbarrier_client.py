
import os
import sys
import time

import argparse

from kazoo.client import KazooClient


import logging
logging.basicConfig ()


class ZK_ClientApp ():
    def __init__ (self, args):
        self.name = args.name
        self.zkIPAddr = args.zkIPAddr  # ZK server IP address
        self.zkPort = args.zkPort # ZK server port num
        self.cond = args.cond # used as barrier condition
        self.ppath = "/barrier" # refers to the parent znode path
        self.zk = None  # session handle to the server
        self.barrier = False  # indicating if barrier has reached
        
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
        """main logic of client"""

        try:
            self.zk.start ()

            while (True):
                if self.zk.exists (self.ppath):
                    print(("ClientApp::run {} - parent znode is set".format (self.name)))
                    # in that case we create our child node
                    self.zk.create (self.ppath + str ("/") + self.name, value=self.name.encode(), ephemeral=True)
                    # make sure to exit the loop
                    break
                else:
                    print(("ClientApp::run {} -- parent znode is not yet up".format (self.name)))
                    time.sleep (1)


            @self.zk.DataWatch (self.ppath)
            def data_change_watcher (data, stat):
                """Data Change Watcher"""
                print(("ClientApp::DataChangeWatcher {} - data = {}, stat = {}".format (self.name, data, stat)))
                value = int (data)
                if (value == self.cond):
                    print(("ClientApp: {}, barrier is reached".format (self.name)))
                    self.barrier = True

            while (self.barrier == False):
                print(("ClientApp {} barrier not reached yet".format (self.name)))
                if self.zk.exists (self.ppath):

                    value,stat = self.zk.get (self.ppath)
                    print(("ClientApp {} found parent znode value = {}, stat = {}".format (self.name, value, stat)))
    
                else:
                    print(("{} znode does not exist yet (strange)".format (self.ppath)))
    
            print(("ClientApp {} has reached the barrier and so we disconnect from zookeeper".format (self.name)))


            self.zk.stop ()
            self.zk.close ()

            print(("ClientApp {}: Bye Bye ".format (self.name)))
    
        except:
            print("Unexpected error in ClientApp::run", sys.exc_info()[0])
            raise
    

def parseCmdLineArgs ():
    parser = argparse.ArgumentParser ()

    parser.add_argument ("-a", "--zkIPAddr", default="127.0.0.1", help="ZooKeeper server ip address, default 127.0.0.1")
    parser.add_argument ("-c", "--cond", type=int, default=5, help="Barrier Condition representing number of client apps in the barrier, default 5")
    parser.add_argument ("-p", "--zkPort", type=int, default=2181, help="ZooKeeper server port, default 2181")
    
    parser.add_argument ("name", help="client name")

    args = parser.parse_args ()

    return args
    

def main ():
    """ Main program """

    print("Demo program for ZooKeeper-based Barrier Sync: Client Appln")
    parsed_args = parseCmdLineArgs ()
    

    client = ZK_ClientApp (parsed_args)

    client.init_client ()
    
    client.run_client ()

#----------------------------------------------
if __name__ == '__main__':
    main ()
