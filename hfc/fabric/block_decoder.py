import logging
import sys

# Import required Peer Protos
from hfc.protos.peer import chaincode_pb2
from hfc.protos.peer import chaincode_event_pb2
from hfc.protos.peer import transaction_pb2
from hfc.protos.peer import proposal_pb2
from hfc.protos.peer import proposal_response_pb2
from hfc.protos.peer import query_pb2
from hfc.protos.peer import configuration_pb2 as peer_configuration_pb2

# Import required MSP Protos
from hfc.protos.msp import msp_principal_pb2
from hfc.protos.msp import msp_config_pb2
from hfc.protos.msp import identities_pb2

# Import required Common Protos
from hfc.protos.common import common_pb2
from hfc.protos.common import configtx_pb2
from hfc.protos.common import policies_pb2
from hfc.protos.common import ledger_pb2
from hfc.protos.common import configuration_pb2 as common_configuration_pb2

# Import required Orderer Protos
from hfc.protos.orderer import configuration_pb2 as orderer_configuration_pb2
from hfc.protos.orderer import ab_pb2

# Import required Ledger Protos
from hfc.protos.ledger.rwset import rwset_pb2
from hfc.protos.ledger.rwset.kvrwset import kv_rwset_pb2


_logger = logging.getLogger(__name__ + ".block_decoder")

# Global Constants
POLICY_POLICYTYPE = ['UNKNOWN', 'SIGNATURE', 'MSP', 'IMPLICIT_META']
IMPLICITMETAPOLICY_RULE = ['ANY', 'ALL', 'MAJORITY']
TYPE_AS_STRING = {
    0: 'MESSAGE',  # Used for messages which are signed but opaque
    1: 'CONFIG',  # Used for messages which express the channel config
    2: 'CONFIG_UPDATE',  # Used for transactions which update the channel config
    3: 'ENDORSER_TRANSACTION',  # Used by the SDK to submit endorser based transactions
    4: 'ORDERER_TRANSACTION',  # Used internally by the orderer for management
    5: 'DELIVER_SEEK_INFO',  # Used as the type for Envelope messages submitted to instruct the Deliver API to seek
    6: 'CHAINCODE_PACKAGE'  # Used for packaging chaincode artifacts for install
}


class BlockDecoder(object):
    """
        An object of a fully decoded protobuf message "Block"
    """

    def decode(self, block_bytes):
        block = {}
        try:
            proto_block = common_pb2.Block  # TODO: decode()
            block['header'] = decode_block_header(proto_block.BlockHeader)
            block['data'] = decode_block_data(proto_block.BlockData)
            block['metadata'] = decode_block_metadata(proto_block.BlockMetadata)
        except:
            e = sys.exc_info()[0]
            _logger.error('BlockDecoder :: decode: {}'.format(e.toString()))

        return block

    def decode_block(self, block_data):
        if not block_data:
            raise ValueError('BlockDecoder :: decode_block: Block input data is missing')
        block = {}
        try:
            block['header'] = {
                'number': str(block_data.number),
                'previous_hash': hex(block_data.previous_hash),
                'data_hash': hex(block_data.data_hash)
            }
            block['data'] = decode_block_data(block_data.data, True)
            block['metadata'] = decode_block_metadata(block_data.metadata)
        except:
            e = sys.exc_info()[0]
            _logger.error('BlockDecoder :: decode_block: {}'.format(e.toString()))

        return block

    def decode_transaction(self, processed_transaction_bytes):
        if not processed_transaction_bytes:
            raise ValueError('BlockDecoder :: decode_transaction: Processed transaction data is missing')
        processed_transaction = {}
        proto_processed_transaction = transaction_pb2.ProcessedTransaction  # TODO: decode()
        processed_transaction['validation_code'] = proto_processed_transaction.TxValidationCode
        processed_transaction['transaction_envelope'] = decode_block_data_envelope(proto_processed_transaction.Transaction)

        return processed_transaction


def decode_block_header(proto_block_header):
    block_header = {}
    block_header['number'] = proto_block_header.number
    block_header['previous_hash'] = proto_block_header.previous_hash
    block_header['data_hash'] = proto_block_header.data_hash
    return block_header


def decode_block_data(proto_block_data, not_proto=None):
    data = {}
    data['data'] = []
    for i in len(proto_block_data.data):
        proto_envelope = None
        if not_proto is not None:
            proto_envelope = common_pb2.Envelope.decode(proto_block_data.data[i])
        else:
            proto_envelope = common_pb2.Envelope.decode(proto_block_data.data[i])  # TODO: toBuffer()
        envelope = decode_block_data_envelope(proto_envelope)
        data['data'].append(envelope)

    return data


def decode_block_metadata(proto_block_metadata):
    metadata = {}
    metadata['metadata'] = []
    if proto_block_metadata and proto_block_metadata.metadata:
        signatures = decode_metadata_signatures(proto_block_metadata.metadata[0])
        metadata['metadata'].append(signatures)

        last_config = decode_last_config_sequence_number(proto_block_metadata.metadata[1])
        metadata['metadata'].append(last_config)

        transaction_filter = decode_transaction_filter(proto_block_metadata.metadata[2])
        metadata['metadata'].append(transaction_filter)

    return metadata


def decode_transaction_filter(metadata_bytes):
    transaction_filter = []
    if not metadata_bytes:
        _logger.debug('BlockDecoder :: decode_transaction_filter: No Metadata')
        return None
    # TODO:
    # Check if metadata_bytes is not an instance of buffer.
    # If it isn't convert it to buffer and store it back.
    _logger.debug('BlockDecoder :: decode_transaction_filter: Metadata length: {}'.format(len(metadata_bytes)))

    for i in range(0, len(metadata_bytes)):
        value = int(metadata_bytes[i])
        _logger.debug('BlockDecoder :: decode_transaction_filter: Looking at index {} with value {}').format(i, value)
        transaction_filter.append(value)

    return transaction_filter


def decode_last_config_sequence_number(metadata_bytes):
    last_config = {}
    last_config['value'] = {}
    if metadata_bytes:
        proto_metadata = common_pb2.Metadata  # TODO: decode()
        proto_last_config = common_pb2.LastConfig  # TODO: decode()
        last_config['value']['index'] = proto_last_config.index
        last_config['signatures'] = decode_metadata_value_signatures(proto_metadata.signatures)
    return last_config


def decode_metadata_signatures(metadata_bytes):
    metadata = {}
    proto_metadata = common_pb2.Metadata  # TODO: decode()
    metadata['value'] = proto_metadata.value
    metadata['signatures'] = decode_metadata_value_signatures(proto_metadata.signatures)
    return metadata


def decode_metadata_value_signatures(proto_metadata_signatures):
    signatures = []
    if proto_metadata_signatures:
        for i in proto_metadata_signatures:
            metadata_signature = {}
            proto_metadata_signature = common_pb2.MetadataSignature  # TODO: decode() toBuffer()
            metadata_signature['signature_header'] = decode_signature_header(proto_metadata_signature.signature_header)
            metadata_signature['signature'] = proto_metadata_signature.signature
            signatures.append(metadata_signature)
    return signatures


def decode_block_data_envelope(proto_envelope):
    envelope = {}
    envelope['signature'] = proto_envelope.SignedTransaction.signature
    envelope['payload'] = {}
    proto_payload = common_pb2.Payload  # TODO: decode()
    envelope['payload']['header'] = decode_header(proto_payload.header)
    # TODO: Implement HeaderType class and it's methods before this.
    # envelope['payload']['data'] =
    # envelope['payload']['header']['channel_header']['type_string'] =
    # TODO: Complete this
    return envelope


def decode_endorser_transaction(trans_bytes):
    pass


def decode_config_envelope(config_envelope_bytes):
    pass


def decode_config(proto_config):
    pass


def decode_config_update_envelope(config_update_envelope_bytes):
    pass


def decode_config_update(config_update_bytes):
    pass


def decode_config_groups(config_group_map):
    pass


def decode_config_group(proto_config_group):
    pass


def decode_config_values(config_value_map):
    pass


def decode_config_value(proto_config_value):
    pass


def decode_config_policies(config_policy_map):
    pass


def decode_config_policy(proto_config_policy):
    pass


def decode_implicit_meta_policy(implicit_meta_policy_bytes):
    pass


def decode_signature_policy_envelope(signature_policy_envelope_bytes):
    pass


def decode_signature_policy(proto_signature_policy):
    pass


def decode_MSP_principal(proto_msp_principal):
    pass


def decode_config_signature(proto_configSignature):
    pass


def decode_signature_header(signature_header_bytes):
    pass


def decode_identity(id_bytes):
    pass


def decode_fabric_MSP_config(msp_config_bytes):
    pass


def decode_fabric_OU_identifier(proto_organizational_unit_identitfiers):
    pass


def to_PEM_certs(buffer_array_in):
    pass


def decode_signing_identity_info(signing_identity_info_bytes):
    pass


def decode_key_info(key_info_bytes):
    pass


def decode_header(proto_header):
    pass


def decode_channel_header(header_bytes):
    pass


def timestamp_to_date(time_stamp):
    pass


def decode_chaincode_action_payload(payload_bytes):
    pass


def decode_chaincode_proposal_payload(chaincode_proposal_payload_bytes):
    pass


def decode_chaincode_endorsed_action(proto_chaincode_endorsed_action):
    pass


def decode_endorsement(proto_endorsement):
    pass


def decode_proposal_response_payload(proposal_response_payload_bytes):
    pass


def decode_chaincode_action(action_bytes):
    pass


def decode_chaincode_events(event_bytes):
    pass


def decode_chaincode_id(proto_chaincode_id):
    pass


def decode_readwrite_sets(rw_sets_bytes):
    pass


def decode_kv_rw_set(kv_bytes):
    pass


def decode_kv_read(proto_kv_read):
    pass


def decode_range_query_info(proto_range_query_info):
    pass


def decode_kv_write(proto_kv_write):
    pass


def decode_response(proto_response):
    pass


def decode_version(version_long):
    pass


# TODO: Add HeaderType class
