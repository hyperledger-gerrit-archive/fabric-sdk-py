import grpc
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

import hfc.protos.peer.events_pb2 as hfc_dot_protos_dot_peer_dot_events__pb2
import hfc.protos.peer.events_pb2 as hfc_dot_protos_dot_peer_dot_events__pb2


class EventsStub(object):
  """Interface exported by the events server
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Chat = channel.stream_stream(
        '/hfc.protos.peer.Events/Chat',
        request_serializer=hfc_dot_protos_dot_peer_dot_events__pb2.Event.SerializeToString,
        response_deserializer=hfc_dot_protos_dot_peer_dot_events__pb2.Event.FromString,
        )


class EventsServicer(object):
  """Interface exported by the events server
  """

  def Chat(self, request_iterator, context):
    """event chatting using Event
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_EventsServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Chat': grpc.stream_stream_rpc_method_handler(
          servicer.Chat,
          request_deserializer=hfc_dot_protos_dot_peer_dot_events__pb2.Event.FromString,
          response_serializer=hfc_dot_protos_dot_peer_dot_events__pb2.Event.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'hfc.protos.peer.Events', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
