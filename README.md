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
Apparantly the following command parser arguments will help:

```python
"-s", "--strategy", default="direct", help="direct or indirect, default direct"
"-i", "--info", default="temp,humidity,pressure", help="chooses the publishing/subscribing informations"
"-z", "--zipcode", default="37209", help="Enter a 5 digit zipcode"
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

If you are working on Assignment 1 make sure to execute the commands in the following order:
- publisher
- broker
- subscriber

In case of the Assignment 2 you are free to use any kind of order. Due to the traffic involved in the broker it is likely to crash which will be rectified soon in Assignment 3.

After Execution you can use the plotting.py to undestand the latency associated with the data transmission.

```python
python plotting.py
```




