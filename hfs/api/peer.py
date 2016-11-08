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

# import grpc
from ..constants import DEFAULT_PEER_GRPC_ADDR
import logging
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from connection import get_connection


class Peer(object):
    """ A peer node in the network.

    It has a specific Grpc channel address.
    """

    def __init__(self, grpc_addr=DEFAULT_PEER_GRPC_ADDR):
        self.logger = logging.getLogger(__name__)
        self.connection = get_connection(grpc_addr)
        self.connection.connect()

    def peer_list(self):
        """list peer on the chain

            return a list of peer nodes currently connected to the target peer.
            The returned  message structure is defined inside api_pb2.proto
            and fabric_pb2.proto.


            ```
            message PeersMessage {
            repeated PeerEndpoint peers = 1;
            }
            message PeerEndpoint {
            PeerID ID = 1;
            string address = 2;
            enum Type {
            UNDEFINED = 0;
            VALIDATOR = 1;
            NON_VALIDATOR = 2;
            }
            Type type = 3;
            bytes pkiID = 4;
            }
            message PeerID {
            string name = 1;
            }
            ```


            :param:empty
            :return:The peer list on the chain
            """

        peer_response = self.connection.stub.GetPeers(
                google_dot_protobuf_dot_empty__pb2.Empty())
        for peer_message in peer_response.peers:
            self.logger.debug("peer information:"
                              "--IDName:{0}"
                              "--address:{1}"
                              "--type:{2}\n".format(peer_message.ID.name,
                                                    peer_message.address,
                                                    peer_message.type))
        return peer_response
