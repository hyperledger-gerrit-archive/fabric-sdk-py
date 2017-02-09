# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hfc/protos/peer/chaincode.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from hfc.protos.peer import chaincodeevent_pb2 as hfc_dot_protos_dot_peer_dot_chaincodeevent__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='hfc/protos/peer/chaincode.proto',
  package='hfc.protos.peer',
  syntax='proto3',
  serialized_pb=_b('\n\x1fhfc/protos/peer/chaincode.proto\x12\x0fhfc.protos.peer\x1a$hfc/protos/peer/chaincodeevent.proto\x1a\x1fgoogle/protobuf/timestamp.proto\")\n\x0b\x43haincodeID\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\"\x1e\n\x0e\x43haincodeInput\x12\x0c\n\x04\x61rgs\x18\x01 \x03(\x0c\"\xf6\x01\n\rChaincodeSpec\x12\x31\n\x04type\x18\x01 \x01(\x0e\x32#.hfc.protos.peer.ChaincodeSpec.Type\x12\x31\n\x0b\x63haincodeID\x18\x02 \x01(\x0b\x32\x1c.hfc.protos.peer.ChaincodeID\x12.\n\x05input\x18\x03 \x01(\x0b\x32\x1f.hfc.protos.peer.ChaincodeInput\x12\x0f\n\x07timeout\x18\x04 \x01(\x05\">\n\x04Type\x12\r\n\tUNDEFINED\x10\x00\x12\n\n\x06GOLANG\x10\x01\x12\x08\n\x04NODE\x10\x02\x12\x07\n\x03\x43\x41R\x10\x03\x12\x08\n\x04JAVA\x10\x04\"\x98\x02\n\x17\x43haincodeDeploymentSpec\x12\x35\n\rchaincodeSpec\x18\x01 \x01(\x0b\x32\x1e.hfc.protos.peer.ChaincodeSpec\x12\x31\n\reffectiveDate\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x13\n\x0b\x63odePackage\x18\x03 \x01(\x0c\x12N\n\x07\x65xecEnv\x18\x04 \x01(\x0e\x32=.hfc.protos.peer.ChaincodeDeploymentSpec.ExecutionEnvironment\".\n\x14\x45xecutionEnvironment\x12\n\n\x06\x44OCKER\x10\x00\x12\n\n\x06SYSTEM\x10\x01\"i\n\x17\x43haincodeInvocationSpec\x12\x35\n\rchaincodeSpec\x18\x01 \x01(\x0b\x32\x1e.hfc.protos.peer.ChaincodeSpec\x12\x17\n\x0fidGenerationAlg\x18\x02 \x01(\t\">\n\x18\x43haincodeProposalContext\x12\x0f\n\x07\x63reator\x18\x01 \x01(\x0c\x12\x11\n\ttransient\x18\x02 \x01(\x0c\"\xc6\x04\n\x10\x43haincodeMessage\x12\x34\n\x04type\x18\x01 \x01(\x0e\x32&.hfc.protos.peer.ChaincodeMessage.Type\x12-\n\ttimestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0f\n\x07payload\x18\x03 \x01(\x0c\x12\x0c\n\x04txid\x18\x04 \x01(\t\x12\x42\n\x0fproposalContext\x18\x05 \x01(\x0b\x32).hfc.protos.peer.ChaincodeProposalContext\x12\x37\n\x0e\x63haincodeEvent\x18\x06 \x01(\x0b\x32\x1f.hfc.protos.peer.ChaincodeEvent\"\xb0\x02\n\x04Type\x12\r\n\tUNDEFINED\x10\x00\x12\x0c\n\x08REGISTER\x10\x01\x12\x0e\n\nREGISTERED\x10\x02\x12\x08\n\x04INIT\x10\x03\x12\t\n\x05READY\x10\x04\x12\x0f\n\x0bTRANSACTION\x10\x05\x12\r\n\tCOMPLETED\x10\x06\x12\t\n\x05\x45RROR\x10\x07\x12\r\n\tGET_STATE\x10\x08\x12\r\n\tPUT_STATE\x10\t\x12\r\n\tDEL_STATE\x10\n\x12\x14\n\x10INVOKE_CHAINCODE\x10\x0b\x12\x0c\n\x08RESPONSE\x10\r\x12\x15\n\x11RANGE_QUERY_STATE\x10\x0e\x12\x17\n\x13\x45XECUTE_QUERY_STATE\x10\x0f\x12\x14\n\x10QUERY_STATE_NEXT\x10\x10\x12\x15\n\x11QUERY_STATE_CLOSE\x10\x11\x12\r\n\tKEEPALIVE\x10\x12\"*\n\x0cPutStateInfo\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c\"3\n\x0fRangeQueryState\x12\x10\n\x08startKey\x18\x01 \x01(\t\x12\x0e\n\x06\x65ndKey\x18\x02 \x01(\t\"\"\n\x11\x45xecuteQueryState\x12\r\n\x05query\x18\x01 \x01(\t\"\x1c\n\x0eQueryStateNext\x12\n\n\x02ID\x18\x01 \x01(\t\"\x1d\n\x0fQueryStateClose\x12\n\n\x02ID\x18\x01 \x01(\t\"0\n\x12QueryStateKeyValue\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c\"m\n\x12QueryStateResponse\x12:\n\rkeysAndValues\x18\x01 \x03(\x0b\x32#.hfc.protos.peer.QueryStateKeyValue\x12\x0f\n\x07hasMore\x18\x02 \x01(\x08\x12\n\n\x02ID\x18\x03 \x01(\t*4\n\x14\x43onfidentialityLevel\x12\n\n\x06PUBLIC\x10\x00\x12\x10\n\x0c\x43ONFIDENTIAL\x10\x01\x32j\n\x10\x43haincodeSupport\x12V\n\x08Register\x12!.hfc.protos.peer.ChaincodeMessage\x1a!.hfc.protos.peer.ChaincodeMessage\"\x00(\x01\x30\x01\x42\x43\n\x16org.hyperledger.protosZ)github.com/hyperledger/fabric/protos/peerb\x06proto3')
  ,
  dependencies=[hfc_dot_protos_dot_peer_dot_chaincodeevent__pb2.DESCRIPTOR,google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_CONFIDENTIALITYLEVEL = _descriptor.EnumDescriptor(
  name='ConfidentialityLevel',
  full_name='hfc.protos.peer.ConfidentialityLevel',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='PUBLIC', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONFIDENTIAL', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1841,
  serialized_end=1893,
)
_sym_db.RegisterEnumDescriptor(_CONFIDENTIALITYLEVEL)

ConfidentialityLevel = enum_type_wrapper.EnumTypeWrapper(_CONFIDENTIALITYLEVEL)
PUBLIC = 0
CONFIDENTIAL = 1


_CHAINCODESPEC_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='hfc.protos.peer.ChaincodeSpec.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNDEFINED', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GOLANG', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NODE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CAR', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='JAVA', index=4, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=383,
  serialized_end=445,
)
_sym_db.RegisterEnumDescriptor(_CHAINCODESPEC_TYPE)

_CHAINCODEDEPLOYMENTSPEC_EXECUTIONENVIRONMENT = _descriptor.EnumDescriptor(
  name='ExecutionEnvironment',
  full_name='hfc.protos.peer.ChaincodeDeploymentSpec.ExecutionEnvironment',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DOCKER', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SYSTEM', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=682,
  serialized_end=728,
)
_sym_db.RegisterEnumDescriptor(_CHAINCODEDEPLOYMENTSPEC_EXECUTIONENVIRONMENT)

_CHAINCODEMESSAGE_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='hfc.protos.peer.ChaincodeMessage.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNDEFINED', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REGISTER', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REGISTERED', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INIT', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='READY', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TRANSACTION', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='COMPLETED', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GET_STATE', index=8, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PUT_STATE', index=9, number=9,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEL_STATE', index=10, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVOKE_CHAINCODE', index=11, number=11,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RESPONSE', index=12, number=13,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RANGE_QUERY_STATE', index=13, number=14,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EXECUTE_QUERY_STATE', index=14, number=15,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='QUERY_STATE_NEXT', index=15, number=16,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='QUERY_STATE_CLOSE', index=16, number=17,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='KEEPALIVE', index=17, number=18,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1180,
  serialized_end=1484,
)
_sym_db.RegisterEnumDescriptor(_CHAINCODEMESSAGE_TYPE)


_CHAINCODEID = _descriptor.Descriptor(
  name='ChaincodeID',
  full_name='hfc.protos.peer.ChaincodeID',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='hfc.protos.peer.ChaincodeID.path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='hfc.protos.peer.ChaincodeID.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=123,
  serialized_end=164,
)


_CHAINCODEINPUT = _descriptor.Descriptor(
  name='ChaincodeInput',
  full_name='hfc.protos.peer.ChaincodeInput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='args', full_name='hfc.protos.peer.ChaincodeInput.args', index=0,
      number=1, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=166,
  serialized_end=196,
)


_CHAINCODESPEC = _descriptor.Descriptor(
  name='ChaincodeSpec',
  full_name='hfc.protos.peer.ChaincodeSpec',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='hfc.protos.peer.ChaincodeSpec.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='chaincodeID', full_name='hfc.protos.peer.ChaincodeSpec.chaincodeID', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='input', full_name='hfc.protos.peer.ChaincodeSpec.input', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='timeout', full_name='hfc.protos.peer.ChaincodeSpec.timeout', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CHAINCODESPEC_TYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=199,
  serialized_end=445,
)


_CHAINCODEDEPLOYMENTSPEC = _descriptor.Descriptor(
  name='ChaincodeDeploymentSpec',
  full_name='hfc.protos.peer.ChaincodeDeploymentSpec',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='chaincodeSpec', full_name='hfc.protos.peer.ChaincodeDeploymentSpec.chaincodeSpec', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='effectiveDate', full_name='hfc.protos.peer.ChaincodeDeploymentSpec.effectiveDate', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='codePackage', full_name='hfc.protos.peer.ChaincodeDeploymentSpec.codePackage', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='execEnv', full_name='hfc.protos.peer.ChaincodeDeploymentSpec.execEnv', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CHAINCODEDEPLOYMENTSPEC_EXECUTIONENVIRONMENT,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=448,
  serialized_end=728,
)


_CHAINCODEINVOCATIONSPEC = _descriptor.Descriptor(
  name='ChaincodeInvocationSpec',
  full_name='hfc.protos.peer.ChaincodeInvocationSpec',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='chaincodeSpec', full_name='hfc.protos.peer.ChaincodeInvocationSpec.chaincodeSpec', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='idGenerationAlg', full_name='hfc.protos.peer.ChaincodeInvocationSpec.idGenerationAlg', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=730,
  serialized_end=835,
)


_CHAINCODEPROPOSALCONTEXT = _descriptor.Descriptor(
  name='ChaincodeProposalContext',
  full_name='hfc.protos.peer.ChaincodeProposalContext',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='creator', full_name='hfc.protos.peer.ChaincodeProposalContext.creator', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='transient', full_name='hfc.protos.peer.ChaincodeProposalContext.transient', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=837,
  serialized_end=899,
)


_CHAINCODEMESSAGE = _descriptor.Descriptor(
  name='ChaincodeMessage',
  full_name='hfc.protos.peer.ChaincodeMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='hfc.protos.peer.ChaincodeMessage.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='hfc.protos.peer.ChaincodeMessage.timestamp', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='payload', full_name='hfc.protos.peer.ChaincodeMessage.payload', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='txid', full_name='hfc.protos.peer.ChaincodeMessage.txid', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='proposalContext', full_name='hfc.protos.peer.ChaincodeMessage.proposalContext', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='chaincodeEvent', full_name='hfc.protos.peer.ChaincodeMessage.chaincodeEvent', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CHAINCODEMESSAGE_TYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=902,
  serialized_end=1484,
)


_PUTSTATEINFO = _descriptor.Descriptor(
  name='PutStateInfo',
  full_name='hfc.protos.peer.PutStateInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='hfc.protos.peer.PutStateInfo.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='hfc.protos.peer.PutStateInfo.value', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1486,
  serialized_end=1528,
)


_RANGEQUERYSTATE = _descriptor.Descriptor(
  name='RangeQueryState',
  full_name='hfc.protos.peer.RangeQueryState',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='startKey', full_name='hfc.protos.peer.RangeQueryState.startKey', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='endKey', full_name='hfc.protos.peer.RangeQueryState.endKey', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1530,
  serialized_end=1581,
)


_EXECUTEQUERYSTATE = _descriptor.Descriptor(
  name='ExecuteQueryState',
  full_name='hfc.protos.peer.ExecuteQueryState',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='query', full_name='hfc.protos.peer.ExecuteQueryState.query', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1583,
  serialized_end=1617,
)


_QUERYSTATENEXT = _descriptor.Descriptor(
  name='QueryStateNext',
  full_name='hfc.protos.peer.QueryStateNext',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ID', full_name='hfc.protos.peer.QueryStateNext.ID', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1619,
  serialized_end=1647,
)


_QUERYSTATECLOSE = _descriptor.Descriptor(
  name='QueryStateClose',
  full_name='hfc.protos.peer.QueryStateClose',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ID', full_name='hfc.protos.peer.QueryStateClose.ID', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1649,
  serialized_end=1678,
)


_QUERYSTATEKEYVALUE = _descriptor.Descriptor(
  name='QueryStateKeyValue',
  full_name='hfc.protos.peer.QueryStateKeyValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='hfc.protos.peer.QueryStateKeyValue.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='hfc.protos.peer.QueryStateKeyValue.value', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1680,
  serialized_end=1728,
)


_QUERYSTATERESPONSE = _descriptor.Descriptor(
  name='QueryStateResponse',
  full_name='hfc.protos.peer.QueryStateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='keysAndValues', full_name='hfc.protos.peer.QueryStateResponse.keysAndValues', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='hasMore', full_name='hfc.protos.peer.QueryStateResponse.hasMore', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ID', full_name='hfc.protos.peer.QueryStateResponse.ID', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1730,
  serialized_end=1839,
)

_CHAINCODESPEC.fields_by_name['type'].enum_type = _CHAINCODESPEC_TYPE
_CHAINCODESPEC.fields_by_name['chaincodeID'].message_type = _CHAINCODEID
_CHAINCODESPEC.fields_by_name['input'].message_type = _CHAINCODEINPUT
_CHAINCODESPEC_TYPE.containing_type = _CHAINCODESPEC
_CHAINCODEDEPLOYMENTSPEC.fields_by_name['chaincodeSpec'].message_type = _CHAINCODESPEC
_CHAINCODEDEPLOYMENTSPEC.fields_by_name['effectiveDate'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_CHAINCODEDEPLOYMENTSPEC.fields_by_name['execEnv'].enum_type = _CHAINCODEDEPLOYMENTSPEC_EXECUTIONENVIRONMENT
_CHAINCODEDEPLOYMENTSPEC_EXECUTIONENVIRONMENT.containing_type = _CHAINCODEDEPLOYMENTSPEC
_CHAINCODEINVOCATIONSPEC.fields_by_name['chaincodeSpec'].message_type = _CHAINCODESPEC
_CHAINCODEMESSAGE.fields_by_name['type'].enum_type = _CHAINCODEMESSAGE_TYPE
_CHAINCODEMESSAGE.fields_by_name['timestamp'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_CHAINCODEMESSAGE.fields_by_name['proposalContext'].message_type = _CHAINCODEPROPOSALCONTEXT
_CHAINCODEMESSAGE.fields_by_name['chaincodeEvent'].message_type = hfc_dot_protos_dot_peer_dot_chaincodeevent__pb2._CHAINCODEEVENT
_CHAINCODEMESSAGE_TYPE.containing_type = _CHAINCODEMESSAGE
_QUERYSTATERESPONSE.fields_by_name['keysAndValues'].message_type = _QUERYSTATEKEYVALUE
DESCRIPTOR.message_types_by_name['ChaincodeID'] = _CHAINCODEID
DESCRIPTOR.message_types_by_name['ChaincodeInput'] = _CHAINCODEINPUT
DESCRIPTOR.message_types_by_name['ChaincodeSpec'] = _CHAINCODESPEC
DESCRIPTOR.message_types_by_name['ChaincodeDeploymentSpec'] = _CHAINCODEDEPLOYMENTSPEC
DESCRIPTOR.message_types_by_name['ChaincodeInvocationSpec'] = _CHAINCODEINVOCATIONSPEC
DESCRIPTOR.message_types_by_name['ChaincodeProposalContext'] = _CHAINCODEPROPOSALCONTEXT
DESCRIPTOR.message_types_by_name['ChaincodeMessage'] = _CHAINCODEMESSAGE
DESCRIPTOR.message_types_by_name['PutStateInfo'] = _PUTSTATEINFO
DESCRIPTOR.message_types_by_name['RangeQueryState'] = _RANGEQUERYSTATE
DESCRIPTOR.message_types_by_name['ExecuteQueryState'] = _EXECUTEQUERYSTATE
DESCRIPTOR.message_types_by_name['QueryStateNext'] = _QUERYSTATENEXT
DESCRIPTOR.message_types_by_name['QueryStateClose'] = _QUERYSTATECLOSE
DESCRIPTOR.message_types_by_name['QueryStateKeyValue'] = _QUERYSTATEKEYVALUE
DESCRIPTOR.message_types_by_name['QueryStateResponse'] = _QUERYSTATERESPONSE
DESCRIPTOR.enum_types_by_name['ConfidentialityLevel'] = _CONFIDENTIALITYLEVEL

ChaincodeID = _reflection.GeneratedProtocolMessageType('ChaincodeID', (_message.Message,), dict(
  DESCRIPTOR = _CHAINCODEID,
  __module__ = 'hfc.protos.peer.chaincode_pb2'
  # @@protoc_insertion_point(class_scope:hfc.protos.peer.ChaincodeID)
  ))
_sym_db.RegisterMessage(ChaincodeID)

ChaincodeInput = _reflection.GeneratedProtocolMessageType('ChaincodeInput', (_message.Message,), dict(
  DESCRIPTOR = _CHAINCODEINPUT,
  __module__ = 'hfc.protos.peer.chaincode_pb2'
  # @@protoc_insertion_point(class_scope:hfc.protos.peer.ChaincodeInput)
  ))
_sym_db.RegisterMessage(ChaincodeInput)

ChaincodeSpec = _reflection.GeneratedProtocolMessageType('ChaincodeSpec', (_message.Message,), dict(
  DESCRIPTOR = _CHAINCODESPEC,
  __module__ = 'hfc.protos.peer.chaincode_pb2'
  # @@protoc_insertion_point(class_scope:hfc.protos.peer.ChaincodeSpec)
  ))
_sym_db.RegisterMessage(ChaincodeSpec)

ChaincodeDeploymentSpec = _reflection.GeneratedProtocolMessageType('ChaincodeDeploymentSpec', (_message.Message,), dict(
  DESCRIPTOR = _CHAINCODEDEPLOYMENTSPEC,
  __module__ = 'hfc.protos.peer.chaincode_pb2'
  # @@protoc_insertion_point(class_scope:hfc.protos.peer.ChaincodeDeploymentSpec)
  ))
_sym_db.RegisterMessage(ChaincodeDeploymentSpec)

ChaincodeInvocationSpec = _reflection.GeneratedProtocolMessageType('ChaincodeInvocationSpec', (_message.Message,), dict(
  DESCRIPTOR = _CHAINCODEINVOCATIONSPEC,
  __module__ = 'hfc.protos.peer.chaincode_pb2'
  # @@protoc_insertion_point(class_scope:hfc.protos.peer.ChaincodeInvocationSpec)
  ))
_sym_db.RegisterMessage(ChaincodeInvocationSpec)

ChaincodeProposalContext = _reflection.GeneratedProtocolMessageType('ChaincodeProposalContext', (_message.Message,), dict(
  DESCRIPTOR = _CHAINCODEPROPOSALCONTEXT,
  __module__ = 'hfc.protos.peer.chaincode_pb2'
  # @@protoc_insertion_point(class_scope:hfc.protos.peer.ChaincodeProposalContext)
  ))
_sym_db.RegisterMessage(ChaincodeProposalContext)

ChaincodeMessage = _reflection.GeneratedProtocolMessageType('ChaincodeMessage', (_message.Message,), dict(
  DESCRIPTOR = _CHAINCODEMESSAGE,
  __module__ = 'hfc.protos.peer.chaincode_pb2'
  # @@protoc_insertion_point(class_scope:hfc.protos.peer.ChaincodeMessage)
  ))
_sym_db.RegisterMessage(ChaincodeMessage)

PutStateInfo = _reflection.GeneratedProtocolMessageType('PutStateInfo', (_message.Message,), dict(
  DESCRIPTOR = _PUTSTATEINFO,
  __module__ = 'hfc.protos.peer.chaincode_pb2'
  # @@protoc_insertion_point(class_scope:hfc.protos.peer.PutStateInfo)
  ))
_sym_db.RegisterMessage(PutStateInfo)

RangeQueryState = _reflection.GeneratedProtocolMessageType('RangeQueryState', (_message.Message,), dict(
  DESCRIPTOR = _RANGEQUERYSTATE,
  __module__ = 'hfc.protos.peer.chaincode_pb2'
  # @@protoc_insertion_point(class_scope:hfc.protos.peer.RangeQueryState)
  ))
_sym_db.RegisterMessage(RangeQueryState)

ExecuteQueryState = _reflection.GeneratedProtocolMessageType('ExecuteQueryState', (_message.Message,), dict(
  DESCRIPTOR = _EXECUTEQUERYSTATE,
  __module__ = 'hfc.protos.peer.chaincode_pb2'
  # @@protoc_insertion_point(class_scope:hfc.protos.peer.ExecuteQueryState)
  ))
_sym_db.RegisterMessage(ExecuteQueryState)

QueryStateNext = _reflection.GeneratedProtocolMessageType('QueryStateNext', (_message.Message,), dict(
  DESCRIPTOR = _QUERYSTATENEXT,
  __module__ = 'hfc.protos.peer.chaincode_pb2'
  # @@protoc_insertion_point(class_scope:hfc.protos.peer.QueryStateNext)
  ))
_sym_db.RegisterMessage(QueryStateNext)

QueryStateClose = _reflection.GeneratedProtocolMessageType('QueryStateClose', (_message.Message,), dict(
  DESCRIPTOR = _QUERYSTATECLOSE,
  __module__ = 'hfc.protos.peer.chaincode_pb2'
  # @@protoc_insertion_point(class_scope:hfc.protos.peer.QueryStateClose)
  ))
_sym_db.RegisterMessage(QueryStateClose)

QueryStateKeyValue = _reflection.GeneratedProtocolMessageType('QueryStateKeyValue', (_message.Message,), dict(
  DESCRIPTOR = _QUERYSTATEKEYVALUE,
  __module__ = 'hfc.protos.peer.chaincode_pb2'
  # @@protoc_insertion_point(class_scope:hfc.protos.peer.QueryStateKeyValue)
  ))
_sym_db.RegisterMessage(QueryStateKeyValue)

QueryStateResponse = _reflection.GeneratedProtocolMessageType('QueryStateResponse', (_message.Message,), dict(
  DESCRIPTOR = _QUERYSTATERESPONSE,
  __module__ = 'hfc.protos.peer.chaincode_pb2'
  # @@protoc_insertion_point(class_scope:hfc.protos.peer.QueryStateResponse)
  ))
_sym_db.RegisterMessage(QueryStateResponse)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\026org.hyperledger.protosZ)github.com/hyperledger/fabric/protos/peer'))
try:
  # THESE ELEMENTS WILL BE DEPRECATED.
  # Please use the generated *_pb2_grpc.py files instead.
  import grpc
  from grpc.framework.common import cardinality
  from grpc.framework.interfaces.face import utilities as face_utilities
  from grpc.beta import implementations as beta_implementations
  from grpc.beta import interfaces as beta_interfaces


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
          request_serializer=ChaincodeMessage.SerializeToString,
          response_deserializer=ChaincodeMessage.FromString,
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
            request_deserializer=ChaincodeMessage.FromString,
            response_serializer=ChaincodeMessage.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'hfc.protos.peer.ChaincodeSupport', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


  class BetaChaincodeSupportServicer(object):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
    """Interface that provides support to chaincode execution. ChaincodeContext
    provides the context necessary for the server to respond appropriately.
    """
    def Register(self, request_iterator, context):
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)


  class BetaChaincodeSupportStub(object):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
    """Interface that provides support to chaincode execution. ChaincodeContext
    provides the context necessary for the server to respond appropriately.
    """
    def Register(self, request_iterator, timeout, metadata=None, with_call=False, protocol_options=None):
      raise NotImplementedError()


  def beta_create_ChaincodeSupport_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This function was
    generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
    request_deserializers = {
      ('hfc.protos.peer.ChaincodeSupport', 'Register'): ChaincodeMessage.FromString,
    }
    response_serializers = {
      ('hfc.protos.peer.ChaincodeSupport', 'Register'): ChaincodeMessage.SerializeToString,
    }
    method_implementations = {
      ('hfc.protos.peer.ChaincodeSupport', 'Register'): face_utilities.stream_stream_inline(servicer.Register),
    }
    server_options = beta_implementations.server_options(request_deserializers=request_deserializers, response_serializers=response_serializers, thread_pool=pool, thread_pool_size=pool_size, default_timeout=default_timeout, maximum_timeout=maximum_timeout)
    return beta_implementations.server(method_implementations, options=server_options)


  def beta_create_ChaincodeSupport_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This function was
    generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
    request_serializers = {
      ('hfc.protos.peer.ChaincodeSupport', 'Register'): ChaincodeMessage.SerializeToString,
    }
    response_deserializers = {
      ('hfc.protos.peer.ChaincodeSupport', 'Register'): ChaincodeMessage.FromString,
    }
    cardinalities = {
      'Register': cardinality.Cardinality.STREAM_STREAM,
    }
    stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer, request_serializers=request_serializers, response_deserializers=response_deserializers, thread_pool=pool, thread_pool_size=pool_size)
    return beta_implementations.dynamic_stub(channel, 'hfc.protos.peer.ChaincodeSupport', cardinalities, options=stub_options)
except ImportError:
  pass
# @@protoc_insertion_point(module_scope)
