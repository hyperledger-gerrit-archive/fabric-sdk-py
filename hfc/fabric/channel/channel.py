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
import random
import sys

from hfc.fabric import user
from hfc.fabric.transaction.tx_context import TXContext
from hfc.fabric.user import validate
from hfc.protos.common import common_pb2
from hfc.protos.orderer import ab_pb2
from hfc.util.utils import proto_str, current_timestamp

SYSTEM_CHANNEL_NAME = ""


class Channel(object):
    """The class represents of the channel. """

    def __init__(self, name, client, is_sys_chan=False):
        self._client = client
        self._orderers = {}
        self._peers = {}
        self._initialized = False
        self._shutdown = False
        self._is_sys_chan = is_sys_chan

        if self._is_sys_chan:
            self._name = SYSTEM_CHANNEL_NAME
            self._initialized = True
        else:
            if not name:
                raise ValueError(
                    "Channel name is invalid can not be null or empty.")
            self._name = name

    def add_orderer(self, orderer):
        """Add orderer endpoint to a chain object.

        A channel instance may choose to use a single orderer node, which
        will broadcast requests to the rest of the orderer network. Or if
        the application does not trust the orderer nodes, it can choose to
        use more than one by adding them to the chain instance. And all
        APIs concerning the orderer will broadcast to all orderers
        simultaneously.

        Args:
             orderer: an instance of the Orderer class
        """
        self._orderers[orderer.endpoint] = orderer

    def remove_orderer(self, orderer):
        """Remove orderer endpoint from a channel object.

        Args:
            orderer: an instance of the Orderer class
        """
        if orderer.endpoint in self._orderers:
            self._orderers.pop(orderer.endpoint, None)

    def add_peer(self, peer):
        """Add peer endpoint to a chain object.

        Args:
             peer: an instance of the Peer class
        """
        self._peers[peer.endpoint] = peer

    def remove_peer(self, peer):
        """Remove peer endpoint from a channel object.

        Args:
            peer: an instance of the Peer class
        """
        if peer.endpoint in self._peers:
            self._peers.pop(peer.endpoint, None)

    @property
    def orderers(self):
        """Get orderers of a channel.

        Returns: The orderer list on the chain
        """
        return self._orderers

    @property
    def peers(self):
        """Get peers of a channel.

        Returns: The peer list on the chain
        """
        return self._peers

    def _get_tx_context(self, user_context=None):
        """Get tx context

        Args:
            user_context (object): user context

        Returns: A tx_context instance

        Raises: ValueError
        """
        user = user_context if not None else self._client.user_context
        validate(user)
        return TXContext(self, user, self._client.crypto_suite)

    def _get_latest_block(self, orderer):
        """ Get latest block from orderer."""
        seek_info = ab_pb2.SeekInfo()
        seek_info.start.newest = ab_pb2.SeekNewest()
        seek_info.stop.newest = ab_pb2.SeekNewest()
        seek_info.behavior = \
            ab_pb2.SeekInfo.SeekBehavior.Value('BLOCK_UNTIL_READY')

        tx_context = self._get_tx_context()
        seek_info_header = build_channel_header(
            common_pb2.HeaderType.Value('DELIVER_SEEK_INFO'),
            tx_context.tx_id, self._name, current_timestamp(),
            tx_context.epoch)

        signature_header = common_pb2.SignatureHeader()
        signature_header.creator = tx_context.identity
        signature_header.nonce = tx_context.nonce

        seek_payload = common_pb2.Payload()
        seek_payload.header.signature_header = \
            signature_header.SerializeToString()
        seek_payload.header.channel_header = \
            seek_info_header.SerializeToString()
        seek_payload.data = seek_info.SerializeToString()

        envelope = common_pb2.Envelope()
        envelope.signature = tx_context.sign(seek_payload.SerializeToString())
        envelope.payload = seek_payload.SerializeToString()

    def _get_random_order(self):
        if sys.version_info < (3, 0):
            return random.choice(self._orderers.values())
        else:
            return random.choice(list(self._orderers.values()))

    def _validate_state(self):
        """Validate channel state.
        
        Raises: 
            ValueError
        
        """
        if self._shutdown:
            raise ValueError(
                "Channel %s has been shutdown.".format(self._name))

        if not self._initialized:
            raise ValueError(
                "Channel %s has not been initialized.".format(self._name))

        user.validate(self._client.user_context)

    @property
    def is_sys_chan(self):
        """Get if system channel"""
        return self._is_sys_chan

    def _validate_peer(self, peer):
        """Validate peer

        Args:
            peer: peer
        
        Raises:
            ValueError
            
        """
        if not peer:
            raise ValueError("Peer value is null.")

        if self._is_sys_chan:
            return

        if peer not in self._peers:
            raise ValueError(
                "Channel %s does not have peer %s".format(self._name,
                                                          peer.endpoint))

        if self not in peer.channels:
            raise ValueError(
                "Peer %s not joined this channel %s".format(peer.endpoint,
                                                            self._name)
            )

    def _validate_peers(self, peers):
        """Validate peer set
        
        Args:
            peers: peers

        Raises:
            ValueError

        """
        if not peers:
            raise ValueError("Collection of peers is null.")

        if len(peers) == 0:
            raise ValueError("Collection of peers is empty.")

        for peer in peers:
            self._validate_peer(peer)

    def send_install_proposal(self, install_proposal_req, peers):
        """ Send install chaincode proposal
        
        Args:
            install_proposal_req: install proposal request
            peers: a set of peer to send

        Returns: a set of proposal response

        """
        self._validate_state()
        self._validate_peers(peers)

        if not install_proposal_req:
            raise ValueError("InstallProposalRequest is null.")

        tx_context = self._get_tx_context(install_proposal_req.user_context)
        tx_context.need_verify(False)
        tx_context.proposal_wait_time(install_proposal_req.proposal_wait_time)


def create_system_channel(client):
    """ Create system channel instance

    Args:
        client: client instance

    Returns: system channel instance

    """
    return Channel(SYSTEM_CHANNEL_NAME, client, True)


def build_channel_header(type, tx_id, channel_id,
                         timestamp, epoch=0, extension=None):
    """Build channel.

    Args:
        extension: extension
        timestamp: timestamp
        channel_id: channel id
        tx_id: transaction id
        type: type
        epoch: epoch

    Returns: common_proto.Header instance

    """
    channel_header = common_pb2.ChannelHeader()
    channel_header.type = type
    channel_header.version = 1
    channel_header.channel_id = proto_str(channel_id)
    channel_header.tx_id = proto_str(tx_id)
    channel_header.epoch = epoch
    channel_header.timestamp = timestamp
    if extension:
        channel_header.extension = extension

    return channel_header
