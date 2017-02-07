# Fabric-SDK-py

**Note:** This is a **read-only mirror** of the formal [Gerrit](https://gerrit.hyperledger.org/r/#/admin/projects/fabric-sdk-py) repository, where active development is ongoing.

Fabric-SDK-py is an implementation of the Hyperledger fabric SDK in Python.

## Incubation Notice

This project is a Hyperledger project in _Incubation_. It was proposed to the community and documented [here](https://docs.google.com/document/d/1N-KbwlFb7Oo_pTG2NjjLTqwlhqp_kjyv5fco7VH8WrE/), and was approved by [Hyperledger TSC at 2016-09-08](http://lists.hyperledger.org/pipermail/hyperledger-tsc/2016-September/000292.html). Information on what _Incubation_ entails can be found in the [Hyperledger Project Lifecycle document](https://goo.gl/4edNRc).

## Bug, Question and Code Contributions
Welcome for any kind of contribution!

Please see [How to Contribution](docs/CONTRIBUTING.md).

# Coding Style

We're following [pep8 style guide](https://www.python.org/dev/peps/pep-0008/) and [Google style](https://google.github.io/styleguide/pyguide.html), please see [coding style](docs/code_style.md)

## Meeting

Weekly scrum meeting will be held at chat channel [#fabric-sdk-python](https://chat.hyperledger.org/channel/fabric-sdk-python/) at 03:00 UTC every Friday. More information, please see the project [wiki](wiki.hyperledger.org/projects/fabric-sdk-py.md).

## Testing
The following command will run the testing.

```sh
$ make check
```

## Generating Docker images
The following command will build a Docker image `hyperledger/fabric-sdk-py` with the fabric-sdk-py installed.

```sh
$ make docker
```

Also, you can use docker-compose to start a cluster for testing, including a fabric peer, an orderer, and an sdk-py container. 

*Note: Currently for the orderer, after you pull the hyperledger/fabric-peer image, you need to retag it to hyperledger/fabric-orderer.*

```sh
$ docker-compose up -d
$ docker exec -it fabric-sdk-py tox
```

## Change Logs
See [Change Log](docs/change_log.md).

## About Hyperledger Project

* [Hyperledger Project](https://www.hyperledger.org)
* [Hyperledger mailing lists and archives](http://lists.hyperledger.org/)
* [Hyperledger Chat](http://chat.hyperledger.org)
* [Hyperledger Wiki](https://github.com/hyperledger/hyperledger/wiki)

## License <a name="license"></a>
The Hyperledger Project uses the [Apache License Version 2.0](LICENSE) software license.
