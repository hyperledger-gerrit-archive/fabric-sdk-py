# Copyright IBM All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0

import logging
from time import sleep

from hfc.fabric.peer import create_peer
from hfc.fabric.transaction.tx_context import create_tx_context
from hfc.fabric.transaction.tx_proposal_request import create_tx_prop_req, \
    CC_TYPE_GOLANG, CC_INSTANTIATE, CC_INSTALL, TXProposalRequest
from hfc.util.crypto.crypto import ecies
from hfc.util.utils import send_transaction, build_tx_req
from test.integration.utils import get_peer_org_user, \
    BaseTestCase
from test.integration.config import E2E_CONFIG
from test.integration.e2e_utils import build_channel_request, \
    build_join_channel_req
from queue import Queue

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
test_network = E2E_CONFIG['test-network']
CC_PATH = 'github.com/example_cc'
CC_NAME = 'example_cc'
CC_VERSION = '1.0'


class ChaincodeInstantiateTest(BaseTestCase):

    def test_instantiate_chaincode(self):

        peer_config = test_network['org1.example.com']['peers']['peer0']
        tls_cacerts = peer_config['tls_cacerts']

        opts = (('grpc.ssl_target_name_override',
                 peer_config['server_hostname']),)

        endpoint = peer_config['grpc_request_endpoint']

        peer = create_peer(endpoint=endpoint,
                           tls_cacerts=tls_cacerts,
                           opts=opts)

        # for chain code install
        tran_prop_req_in = create_tx_prop_req(
            prop_type=CC_INSTALL,
            cc_path=CC_PATH,
            cc_type=CC_TYPE_GOLANG,
            cc_name=CC_NAME,
            cc_version=CC_VERSION
        )

        # for chain code deploy
        args = ['a', '100', 'b', '40']
        tran_prop_req_dep = create_tx_prop_req(
            prop_type=CC_INSTANTIATE,
            cc_type=CC_TYPE_GOLANG,
            cc_name=CC_NAME,
            cc_version=CC_VERSION,
            fcn='init',
            args=args
        )

        org1 = 'org1.example.com'
        crypto = ecies()
        org1_admin = get_peer_org_user(org1, 'Admin',
                                       self.client.state_store)

        # create a channel
        request = build_channel_request(self.client,
                                        self.channel_tx,
                                        self.channel_name)

        self.client._create_channel(request)
        sleep(5)

        # join channel
        channel = self.client.new_channel(self.channel_name)
        join_req = build_join_channel_req(org1, channel, self.client)
        channel.join_channel(join_req)
        sleep(5)

        # install chain code
        tx_context_in = create_tx_context(org1_admin,
                                          crypto,
                                          tran_prop_req_in)

        self.client.send_install_proposal(tx_context_in, [peer])
        sleep(5)

        # deploy the chain code
        tx_context_dep = create_tx_context(org1_admin,
                                           crypto,
                                           tran_prop_req_dep)
        res = channel.send_instantiate_proposal(tx_context_dep, [peer])
        sleep(5)

        # send the transaction to the channel
        tx_context = create_tx_context(org1_admin,
                                       crypto,
                                       TXProposalRequest())
        tran_req = build_tx_req(res)
        response = send_transaction(channel.orderers, tran_req, tx_context)

        q = Queue(1)
        response.subscribe(on_next=lambda x: q.put(x),
                           on_error=lambda x: q.put(x))
        res, _ = q.get(timeout=10)
        logger.debug(res)
        self.assertEqual(res.status, 200)
