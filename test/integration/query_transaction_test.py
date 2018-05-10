# Copyright IBM ALL Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0


import sys
import logging
from time import sleep

from hfc.fabric.peer import create_peer
from hfc.fabric.transaction.tx_context import create_tx_context
from hfc.fabric.transaction.tx_proposal_request import TXProposalRequest
from hfc.util.crypto.crypto import ecies
from test.integration.utils import get_peer_org_user,\
    BaseTestCase
from test.integration.config import E2E_CONFIG
from test.integration.e2e_utils import build_channel_request,\
    build_join_channel_req

if sys.version_info < (3, 0):
    from Queue import Queue
else:
    from queue import Queue

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
test_network = E2E_CONFIG['test-network']


class QueryTransaction(BaseTestCase):
    def test_query_transaction_id_fail(self):
        self.channel = self.client.new_channel(self.channel_name)
        org1 = "org1.example.com"
        peer_config = test_network['org1.example.com']['peers']['peer0']
        tls_cacerts = peer_config['tls_cacerts']
        opts = (('grpc.ssl_target_name_override',
                 peer_config['server_hostname']),)
        endpoint = peer_config['grpc_request_endpoint']
        self.org1_peer = create_peer(endpoint=endpoint,
                                     tls_cacerts=tls_cacerts,
                                     opts=opts)
        self.org1_admin = get_peer_org_user(org1,
                                            "Admin",
                                            self.client.state_store)
        request = build_channel_request(self.client,
                                        self.channel_tx,
                                        self.channel_name)
        self.client._create_channel(request)
        sleep(5)

        join_req = build_join_channel_req(org1, self.channel, self.client)
        self.channel.join_channel(join_req)
        sleep(5)
        tx_context = create_tx_context(self.org1_admin,
                                       ecies(),
                                       TXProposalRequest())
        # pass randomly generated tx_id to the method
        response = self.channel.query_transaction_by_id(tx_context, [self.org1_peer],
                                                        tx_context._tx_id)
        q = Queue(1)
        # on error put 1 or else 0
        response.subscribe(on_next=lambda x: q.put(0),
                           on_error=lambda x: q.put(1))
        res = q.get(timeout=5)
        self.assertEqual(res, 1)
