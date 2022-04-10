
import sys


from kazoo.client import KazooClient


print ("Instantiating a KazooClient object")
zk = KazooClient (hosts = "127.0.0.1:2181")
print ("client current state = {}".format (zk.state))


@zk.DataWatch("/foo")
def watch_data_change (data, stat):
    print ("\n*********** Inside watch_data_change *********")
    print ("Data changed for znode /foo: data = {}, stat = {}".format (data,stat))
    print ("*********** Leaving watch_data_change *********")


try:

    print ("Connecting to the ZooKeeper Server")
    zk.start ()
    print ("client current state = {}".format (zk.state))

    input ("Press any key to continue")


    print ("Creating an ephemeral znode /foo with value bar")
    zk.create ("/foo", value="bar", ephemeral=True, makepath=True)
    print ("client current state = {}".format (zk.state))

    input ("Press any key to continue")


    print ("Checking if /foo exists (it better be)")
    if zk.exists ("/foo"):
        print ("/foo znode indeed exists")

        value,stat = zk.get ("/foo", watch=watch_data_change)
        print ("Details of /foo: value = {}, stat = {}".format (value, stat))
        
    else:
        print ("/foo znode does not exist, why?")
    
    input ("Press any key to continue")

    print ("Setting a new value on znode /foo")
    if zk.exists ("/foo"):
        print ("/foo znode still exists :-)")

        zk.set ("/foo", b"bar2")

        value,stat = zk.get ("/foo")
        print ("Details of /foo: value = {}, stat = {}".format (value, stat))
        
    else:
        print ("/foo znode does not exist, why?")
    
    input ("Press any key to continue")

    print ("Disconnecting")
    zk.stop ()
    print ("client current state = {}".format (zk.state))

    input ("Press any key to continue")


    print ("Reconnecting")
    zk.start ()
    print ("client current state = {}".format (zk.state))

    input ("Press any key to continue")

    print ("Checking if /foo still exists")
    if zk.exists ("/foo"):
        print ("/foo znode still exists -- not possible")
    else:
        print ("/foo znode no longer exists")

    input ("Press any key to continue")

    print ("Disconnecting")
    zk.stop ()
    print ("client current state = {}".format (zk.state))

    print ("Cleaning up")
    zk.close ()
    print ("client current state = {}".format (zk.state))
    
except:
        print ("Exception thrown: ", sys.exc_info()[0])

