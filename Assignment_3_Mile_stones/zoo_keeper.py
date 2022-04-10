from useful_fns import *

def main ():
    """ Main program """

    print("Demo program for ZooKeeper-based Barrier Sync")
    parsed_args = parseCmdLineArgs ()
    
    driver = ZK_Driver (parsed_args)

    driver.init_driver ()
    
    driver.run_driver ()

if __name__ == '__main__':
    main ()