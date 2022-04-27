# DS_REPO

DS_REPO is a python based project folder where Zero MQ experiments are being conducted and experimented. To use the repo one has to have a linux based system with mininet installed.
Please refer to the following instructions for using this repo. All codes are inside the Mile_stones folder.


## Installation
[Mini-net](http://mininet.org/download/)

Prefer the following bash scripting with your python preferences.

```bash
git clone https://github.com/mininet/mininet
sudo PYTHON=python3 mininet/util/install.sh -n 
```
for easy and error free installation.
## Usage

Create a network using the mininet command and a suitable topology:

```bash
sudo mn --topo=tree,depth=3,fanout=3
```
Once the network is up and running, follow the commands given in the command.txt file to execute it line by line on the mininet bash preferably in the background.
Example:

```bash
h1 python -u registry_server.py -s indirect &> ./logs/registry.logs.out &
```
One can get necessary help by typing -h with any python code:
```python
python registry_server.py -h
```
Apparantly the following command parser arguments will help and the compulsory ones are marked important:

```python
"-s", "--strategy", default="direct", help="direct or indirect, default direct" #important
"-i", "--info", default="temp,humidity,pressure",help="give the publishing information in order"
"-z", "--zipcode", default="37209", help="Enter a 5 digit zipcode"
"-d", "--debug", default=logging.WARNING, action="store_true",help="Logging level (see logging package): default WARNING else DEBUG"
"-a", "--ipaddr", type=str, default=None, help="IP address of any existing DHT node"
"-p", "--port", help="port number used by one or more DHT nodes", type=int, default=8468
"-o", "--override_port",help="overriden port number used by our node. Used if we want to create many nodes on the same host",type=int, default=None
"-k", "--key", type=str, default=None, help="Key to set value under"
"-v", "--value", type=str, default=None, help="value for the key to set under"
"-t", "--duration", type=int, default=1000, help="duration of a publisher"
"-zka", "--zkIPAddr", default="127.0.0.1", help="ZooKeeper server ip address, default 127.0.0.1" #important
"-zkp", "--zkPort", type=int, default=2181, help="ZooKeeper server port, default 2181"
"name", default = "None", help="client name" #important and need to make sure that the names are unique
```

Alternatively you can run:
```bash
source command.txt
```
to execute all the commands in order.

The above commands can also be run on individual nodes after going to their corresponding xterms which you can open by the command:

```bash
xterm h1
```
which will open the xterm corresponding to node h1 where you can directly run the python script.

Make sure to always execute the registry_server on the node h1. The network is hosted with the registry information running on host 1. The rest of the commands you are free to execute on any node. 

```python
python plotting.py
```




