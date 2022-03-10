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



def main ():
	# Linear = LinearTopo(k=4)
	# net = Mininet(topo=Linear)
	net = Mininet()
	c0 = net.addController('c0')
	h0 = net.addHost('h0')
	s0 = net.addSwitch('s0')
	h1 = net.addHost('h1')

	net.addLink(h0,s0)
	net.addLink(s0,h1)

	print("Activate network")
	net.start()
	# net.startTerms()

	print("Network Activated")


	# dumpNodeConnections(net.hosts)

	h0.cmd('python pub.py &> publisher_details.out &')
	h1.cmd('python sub.py 10.0.0.1 &> subscriber_details.out &')
	# h = net.get('h0')
	# result_h1 = h1.waitOutput()
	# result_h0 = h1.waitOutput()
	# result0 = h0.cmd('ifconfig')
	# result1 = h1.cmd('ifconfig')
	# print(result0,result1,result_h1)


	print("Exection sent to background and now awaiting the results from the publisher")


	# print(net.hosts)

	# CLI(net)
	# net.pingAll()
	# net.stop()




if __name__ == '__main__':
    main ()