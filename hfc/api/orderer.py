# Copyright IBM Corp. 2017 All Rights Reserved.
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

from hfc.protos.orderer import ab_pb2
from hfc.util.channel import channel

DEFAULT_ORDERER_ENDPOINT = 'localhost:7050'

_logger = logging.getLogger(__name__ + ".orderer")


class Orderer(object):
    """ A orderer node in the network.

    It has a specific Grpc channel address.
    """

    def __init__(self, endpoint=DEFAULT_ORDERER_ENDPOINT,
                 pem=None, opts=None):
        self._endpoint = endpoint
        self._orderer_client = ab_pb2.AtomicBroadcastStub(
            channel(self._endpoint, pem, opts))

    def broadcast(self, envelope):
        """ Send an broadcast envelope to orderer

        Args:
            envelope: The message envelope

        Returns: orderer_response or exception

        """
        _logger.debug("Send envelope={}".format(envelope))
        return self._orderer_client.Broadcast(envelope)

    def delivery(self, envelope):
        """ Send an delivery envelop to orderer

        Args:
            envelope: The message envelope

        Returns: orderer_response or exception

        """
        _logger.debug("Send envelope={}".format(envelope))
        return self._orderer_client.Deliver(envelope)

    @property
    def endpoint(self):
        """Return the endpoint of the orderer.

        Returns: endpoint

        """
        return self._endpoint
