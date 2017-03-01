import grpc
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

import hfc.protos.peer.chaincodeshim_pb2 as hfc_dot_protos_dot_peer_dot_chaincodeshim__pb2
import hfc.protos.peer.chaincodeshim_pb2 as hfc_dot_protos_dot_peer_dot_chaincodeshim__pb2


class ChaincodeSupportStub(object):
  """Interface that provides support to chaincode execution. ChaincodeContext
  provides the context necessary for the server to respond appropriately.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Register = channel.stream_stream(
        '/hfc.protos.peer.ChaincodeSupport/Register',
        request_serializer=hfc_dot_protos_dot_peer_dot_chaincodeshim__pb2.ChaincodeMessage.SerializeToString,
        response_deserializer=hfc_dot_protos_dot_peer_dot_chaincodeshim__pb2.ChaincodeMessage.FromString,
        )


class ChaincodeSupportServicer(object):
  """Interface that provides support to chaincode execution. ChaincodeContext
  provides the context necessary for the server to respond appropriately.
  """

  def Register(self, request_iterator, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ChaincodeSupportServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Register': grpc.stream_stream_rpc_method_handler(
          servicer.Register,
          request_deserializer=hfc_dot_protos_dot_peer_dot_chaincodeshim__pb2.ChaincodeMessage.FromString,
          response_serializer=hfc_dot_protos_dot_peer_dot_chaincodeshim__pb2.ChaincodeMessage.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'hfc.protos.peer.ChaincodeSupport', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
