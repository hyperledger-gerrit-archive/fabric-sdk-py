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
import re
import sys
import uuid
import logging
from hashlib import sha256

from hfc.protos.common import common_pb2
from hfc.protos.utils import create_seek_info, create_seek_payload, \
    create_envelope
from hfc.util.utils import current_timestamp, \
    build_header, build_channel_header, pem_to_der
from hfc.fabric.transaction.tx_context import TXContext
from hfc.fabric.transaction.tx_proposal_request import TXProposalRequest
from hfc.fabric.block_decoder import BlockDecoder, FilteredBlockDecoder

_logger = logging.getLogger(__name__ + ".channel_eventhub")


class ChannelEventHub(object):
    """A class represents channel event hub."""

    def __init__(self, peer, channel_name, requestor):
        self._peer = peer
        self._requestor = requestor
        self._channel_name = channel_name
        self._events = None
        self._filtered = True
        self._reg_nums = []
        self._tx_ids = []
        self._reg_ids = []
        self._connected = False

    def _get_events(self, start=None, stop=None, filtered=True,
                    behavior='BLOCK_UNTIL_READY'):
        """ get the events of the channel.
        Return: the events in success or None in fail.
        """
        _logger.info("get events")

        seek_info = create_seek_info(start, stop, behavior)

        kwargs = {}
        if self._peer._client_cert_path:
            with open(self._peer._client_cert_path, 'rb') as f:
                b64der = pem_to_der(f.read())
                kwargs['tls_cert_hash'] = sha256(b64der).digest()

        tx_context = TXContext(self._requestor, self._requestor.cryptoSuite,
                               TXProposalRequest())

        seek_info_header = build_channel_header(
            common_pb2.HeaderType.Value('DELIVER_SEEK_INFO'),
            tx_context.tx_id,
            self._channel_name,
            current_timestamp(),
            tx_context.epoch,
            **kwargs
        )

        seek_header = build_header(
            tx_context.identity,
            seek_info_header,
            tx_context.nonce)

        seek_payload_bytes = create_seek_payload(seek_header, seek_info)
        sig = tx_context.sign(seek_payload_bytes)
        envelope = create_envelope(sig, seek_payload_bytes)

        # this is a stream response
        return self._peer.delivery(envelope, filtered=filtered)

    async def _handle_block_events(self, reg_num):
        async for event in self._events:
            if reg_num not in self._reg_nums:
                break

            yield event

    def registerBlockEvent(self):
        reg_num = str(uuid.uuid4())
        self._reg_nums.append(reg_num)
        return reg_num, self._handle_block_events(reg_num)

    def unregisterBlockEvent(self, reg_num):
        self._reg_nums.remove(reg_num)

    async def registerTxEvent(self, tx_id):
        self._tx_ids.append(tx_id)
        async for event in self._events:

            # check if not been removed by timeout
            if tx_id not in self._tx_ids:
                break

            if self._filtered:
                event = FilteredBlockDecoder().decode(
                    event.filtered_block.SerializeToString())
            else:
                event = BlockDecoder().decode(event.block.SerializeToString())

            for ft in event['filtered_transactions']:
                if tx_id == ft['txid']:
                    if ft['tx_validation_code'] == 'VALID':
                        return event
                    else:
                        raise Exception('invalid')

    def unregisterTxEvent(self, tx_id):
        self._tx_ids.remove(tx_id)

    async def _handle_chaincode_events(self, reg_id, ccid, pattern):
        async for event in self._events:
            # check if not been removed by timeout
            if reg_id not in self._reg_ids:
                break

            if self._filtered:
                event = FilteredBlockDecoder().decode(
                    event.filtered_block.SerializeToString())
            else:
                event = BlockDecoder().decode(event.block.SerializeToString())

            if 'data' in event:
                data = event['data']['data'][0]['payload']['data']
                action = data['actions'][0]['payload']['action']
                ppl_r_p = action['proposal_response_payload']
                events = ppl_r_p['extension']['events']
                if events['chaincode_id'] == ccid and\
                        re.match(pattern, events['event_name']):
                    return event

    def registerChaincodeEvent(self, ccid, pattern):
        reg_id = str(uuid.uuid4())
        self._reg_ids.append(reg_id)
        return reg_id, self._handle_chaincode_events(reg_id, ccid, pattern)

    def unregisterChaincodeEvent(self, reg_id):
        self._reg_ids.remove(reg_id)

    def connect(self, filtered=True, start=None, stop=sys.maxsize,
                behavior='BLOCK_UNTIL_READY'):
        self._filtered = filtered
        self._events = self._get_events(start=start, stop=stop,
                                        filtered=self._filtered,
                                        behavior=behavior)
        self._connected = True

    def disconnect(self):
        self._events = None
        self._filtered = True
        self._peer = None
        self._requestor = None
        self._channel_name = None
        self._connected = False
