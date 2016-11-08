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
import grpc
from ..protos import api_pb2


class Connection(object):

    def __init__(self, grpc_address):
        """ Connection object - Used in nodes and peers in the network.

        Args:
            grpc_address (str): The GRPC address for the connection
        """
        self.logger = logging.getLogger(__name__)
        self.grpc_addr = grpc_address
        self.channel = grpc.insecure_channel(grpc_address)

    def connect(self):
        """ Connect to the channel setup for the GRPC address
        """
        try:
            self.stub = api_pb2.OpenchainStub(self.channel)
            self.logger.info("Connected to channel on %s" % (self.grpc_addr))
        except:
            self.logger.error("Unable to connect to %s" % self.grpc_addr,
                              exc_info=1)


def get_connection(grpc_address):
    """ Factory method for connecting nodes and peers in a blockchain/orderer
        network.

        Args:
            grpc_address (str): GRPC address

        Returns:
            object: a Connection instance that will be used to communicate with
    """
    return Connection(grpc_address)
