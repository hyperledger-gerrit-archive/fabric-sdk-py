# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

import hfc.protos.gossip.message_pb2 as hfc_dot_protos_dot_gossip_dot_message__pb2


class GossipStub(object):
  """Gossip
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GossipStream = channel.stream_stream(
        '/hfc.protos.gossip.Gossip/GossipStream',
        request_serializer=hfc_dot_protos_dot_gossip_dot_message__pb2.Envelope.SerializeToString,
        response_deserializer=hfc_dot_protos_dot_gossip_dot_message__pb2.Envelope.FromString,
        )
    self.Ping = channel.unary_unary(
        '/hfc.protos.gossip.Gossip/Ping',
        request_serializer=hfc_dot_protos_dot_gossip_dot_message__pb2.Empty.SerializeToString,
        response_deserializer=hfc_dot_protos_dot_gossip_dot_message__pb2.Empty.FromString,
        )


class GossipServicer(object):
  """Gossip
  """

  def GossipStream(self, request_iterator, context):
    """GossipStream is the gRPC stream used for sending and receiving messages
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Ping(self, request, context):
    """Ping is used to probe a remote peer's aliveness
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_GossipServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GossipStream': grpc.stream_stream_rpc_method_handler(
          servicer.GossipStream,
          request_deserializer=hfc_dot_protos_dot_gossip_dot_message__pb2.Envelope.FromString,
          response_serializer=hfc_dot_protos_dot_gossip_dot_message__pb2.Envelope.SerializeToString,
      ),
      'Ping': grpc.unary_unary_rpc_method_handler(
          servicer.Ping,
          request_deserializer=hfc_dot_protos_dot_gossip_dot_message__pb2.Empty.FromString,
          response_serializer=hfc_dot_protos_dot_gossip_dot_message__pb2.Empty.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'hfc.protos.gossip.Gossip', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
