import grpc
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from ..constants import DEFAULT_PEER_GRPC_ADDR
import sys
sys.path.append('../protos')
import api_pb2


class Peer(object):
    """ A peer node in the network.

    It has a specific Grpc channel address.
    """

    def __init__(self, grpc_addr=DEFAULT_PEER_GRPC_ADDR):
        self.grpc_addr = grpc_addr

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

        channel = grpc.insecure_channel(self.grpc_addr)
        peer_stub = api_pb2.OpenchainStub(channel)
        peer_response = peer_stub.GetPeers(
                        google_dot_protobuf_dot_empty__pb2.Empty())
        peer_num = len(peer_response.peers)
        for i in range(peer_num):
            print("peer information:--IDName:%s--address:%s--type:%s\n" % (
                   peer_response.peers[i].ID.name,
                   peer_response.peers[i].address,
                   peer_response.peers[i].type))
        return peer_response
