import os              
import sys            
import random          
import time

from mininet.topo import LinearTopo
from mininet.util import dumpNodeConnections
from mininet.net import CLI
from mininet.term import makeTerm
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.term import makeTerm



def main ():
	net = Mininet()
	c0 = net.addController()
	s0 = net.addSwitch('s0')
	h0 = net.addHost('h0')
	h1 = net.addHost('h1')
	h2 = net.addHost('h2')
	h3 = net.addHost('h3')

	net.addLink(h0,s0)
	net.addLink(h1,s0)
	net.addLink(h2,s0)
	net.addLink(h3,s0)

	print("Activate network")
	net.start()
	# net.startTerms()
	net.start()
	time.sleep(3)
	net.pingAll()
	print("Network Activated")


	h0.cmd('python -u registry_server.py & > registry.logs.out &')
	time.sleep(1)
	h1.cmd('python -u publisher_poller.py & > publisher_37209_all.logs.out &')
	time.sleep(1)
	h2.cmd('python -u broker.py & > broker.logs.out &')
	time.sleep(1)
	h3.cmd('python -u subscriber_poller.py & > subscriber_37209_all.logs.out &')
	time.sleep(10)
	# print("Exection sent to background and now awaiting the results from the publisher ")
	# # net.monitor()
	# net.stop()
	# CLI(net)



if __name__ == '__main__':
    main ()