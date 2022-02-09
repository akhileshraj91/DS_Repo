import os              # OS level utilities
import sys             # system level utilities
import random          # random number generator

from time import time

from mininet.net import Mininet
from mininet.topo import LinearTopo
from mininet.util import dumpNodeConnections
from mininet.net import CLI
from mininet.term import makeTerm
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.term import makeTerm


	


my_ip = h1.cmd('python pub.py &> publisher_details.out &')
print(my_ip)