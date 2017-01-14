import os
import time
import unittest

from test.unit.util import cli_call
from hfc.api.peer import Peer


def add_one(x):
    return x + 1


class DemoTest(unittest.TestCase):
    """ This is an example framework for test case
    """
    def setUp(self):
        self.name = b'Hello world!'

    @staticmethod
    def start_test_env():
        cli_call(["docker-compose", "-f",
                  os.path.join(os.path.dirname(__file__),
                               "../fixtures/chaincode/docker-compose.yml"),
                  "up", "-d"])

    @staticmethod
    def shutdown_test_env():
        cli_call(["docker-compose", "-f",
                  os.path.join(os.path.dirname(__file__),
                               "../fixtures/chaincode/docker-compose.yml"),
                  "stop"])
        cli_call(["docker-compose", "-f",
                  os.path.join(os.path.dirname(__file__),
                               "../fixtures/chaincode/docker-compose.yml"),
                  "kill"])
        cli_call(["docker-compose", "-f",
                  os.path.join(os.path.dirname(__file__),
                               "../fixtures/chaincode/docker-compose.yml"),
                  "rm", "-f"])

    def test_deploy(self):
        self.start_test_env()
        time.sleep(5)
        grpc_addr = os.environ.get('GRPC_ADDR','localhost:7050')
        peer = Peer(grpc_addr=grpc_addr)
        peer
        self.shutdown_test_env()
        self.assertEqual(add_one(3), 4)

if __name__ == '__main__':
    unittest.main()
