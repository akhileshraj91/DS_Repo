import netifaces
import argparse

def get_default_addr():
    for interface in netifaces.interfaces():
        # Skip loopback interface for now
        if interface.startswith("lo"):
            continue

        addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addrs and len(addrs[netifaces.AF_INET]) > 0:
            return addrs[netifaces.AF_INET][0]["addr"]
    return "127.0.0.1"


def get_key(val):
    for key, value in my_dict.items():
         if val == value:
             return key


def parseCmdLineArgs ():
    parser = argparse.ArgumentParser ()
    parser.add_argument ("-s", "--strategy", default="indirect")
    args = parser.parse_args ()
    return args
    
