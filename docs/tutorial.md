# Tutorial of using Fabric SDK

**Notice: The tutorial is still in-progress.**

## Pre-requisites

### Install Fabric SDK

```bash
$ git clone https://github.com/hyperledger/fabric-sdk-py.git
$ cd fabric-sdk-py
$ python setup.py install
```

After installation, you can optionally verify the installation.

```bash
$ python
>>> import hfc
>>> print(hfc.VERSION)
0.0.1
```

### Start a Fabric Network

SDK needs a targeted fabric network to operate with, if there is not a running one, need to start a network manually.

To start a fabric network you can simple up the `docker-compose-2orgs-4peers-tls` under fixtures.

```bash
docker-compose -f test/fixtures/docker-compose-2orgs-4peers-tls.yaml up
```

Then you'll have 2 orgs (org1.example.com; org2.example.com) with 2 peers in each one and one orderer (orderer.example.com)

If you want to understand the fabric-network and how to change the network configuration, we'd recommend you to follow the byfn tutorial, from [this point](http://hyperledger-fabric.readthedocs.io/en/release/build_network.html#crypto-generator)
[to here](http://hyperledger-fabric.readthedocs.io/en/release/build_network.html#start-the-network), you don't need the cli
service on the yaml file either.

### Create Connection Profile

A network connection profile will include all information that SDK requires to operate with a fabric network, including:

* Service endpoints for peer, orderer, ca;
* Credentials for identities that clients may act as;

e.g., `network1.json`.

## Load Configurations

SDK can load all network information from the profile, and check the resources in the network.

```python
# TODO: update code
import hfc

cli = hfc.Client()
cli.load_config("./network1.json")

cli.list_users()  # local valid users that can be used as client role
cli.list_peers()  # peers in the network
cli.list_orderers()  # orderers in the network
cli.list_cas()  # ca nodes in the network
```

## Interaction with Fabric Network

After load the configuration, SDK can operate with the network.

### Create a New Channel
```python
# TODO: update code
cli.create_channel(user_id, channel_name)
```

### Join Peers into Channel

### Install Chaincode to Peers

### Instantiate Chaincode in Channel

### Invoke a Chaincode

## License <a name="license"></a>

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This document is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
