from useful_fns import *


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