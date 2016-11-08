# Copyright IBM Corp. 2016 All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging
from socket import socket


class Connection(object):

    def __init__(self, address, port):
        """ Connection object - Used in nodes and peers in the network.

        Args:
            address (str): The IP address for the connection
            port (int): The port to connect to
        """
        self.logger = logging.getLogger(__name__)
        self.address = address
        self.port = port
        self.sock = socket.socket()

    def connect(self):
        """ Connect to the address and port specified
        """
        try:
            self.sock.connect((self.address, self.port))
            self.logger.info("Connected to %s:%d" % (self.address, self.port))
        except
            self.logger.error("Unable to connect to %s:%d" % (self.address, self.port), exc_info=1)

    def close(self):
        """ Close the connection to the address and port specified
        """
        self.sock.close()
        self.logger.info("Closed connection to %s:%d" % (self.address, self.port))


def connection(address, port):
    """ Factory method for connecting nodes and peers in a blockchain/orderer network.
        Args:
            address (str): IP address
            port (int): port number

        Returns:
            object: a connection instance using the address and port
        """
        return Connection(address, port)
