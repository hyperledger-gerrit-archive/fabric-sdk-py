"""
# Licensed under the Apache License, Version 2.0 (the "License")
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
"""

import unittest
import logging
import os

from hfc.fabric.client import Client
from hfc.fabric.tx_context import TXContext
from hfc.fabric.crypto.crypto import Ecies
from hfc.fabric.util.keyvaluestore import FileKeyValueStore
from hfc.fabric.util import utils

from test.unit.util import get_orderer_admin, get_peer_org_admin
from test.unit.util import cli_call
from test.itergration.e2e_config import E2E_CONFIG
_logger = logging.getLogger("E2E TEST:" + __file__)


class CreateChannelTest(unittest.TestCase):

    def setUp(self):

        self.base_path = "/tmp/fabric-sdk-py"
        self.kv_store_path = os.path.join(self.base_path, "key-value-store")
        self.channel_tx = \
            E2E_CONFIG['test-network']['channel-artifacts']['channel_tx']
        self.channel_name = \
            E2E_CONFIG['test-network']['channel-artifacts']['channel_id']
        self.compose_file_path = \
            E2E_CONFIG['test-network']['docker']['compose-file_tls']

        self.start_test_env()

    def tearDown(self):

        self.kv_store_path = None
        self.shutdown_test_env()

    def start_test_env(self):

        cli_call(["docker-compose", "-f", self.compose_file_path, "up", "-d"])

    def shutdown_test_env(self):

        cli_call(["docker-compose", "-f", self.compose_file_path, "down"])

    def test_create_channel(self):

        signatures = []
        client = Client()
        client.state_store = FileKeyValueStore(self.kv_store_path)
        config = utils.extract_channel_config(self.channel_tx)

        orderer_config = E2E_CONFIG['test-network']['orderer']
        with open(orderer_config['tls-cacerts'], 'rb') as tls_cacerts:
            pem = tls_cacerts.read()

        orderer = client.new_orderer({'endpoint': orderer_config['endpoint'],
                                      'pem': pem,
                                      'opts': None
                                      })
        orderer_admin = get_orderer_admin(client)
        orderer_tx_context = TXContext(orderer_admin, Ecies())
        client.tx_context = orderer_tx_context
        orderer_admin_signature = client.sign_channel_config(config)
        orderer_admin_signature_bytes = \
            orderer_admin_signature.SerializeToString()
        signatures.append(orderer_admin_signature_bytes)
        tx_id = orderer_tx_context.tx_id
        nonce = orderer_tx_context.nonce

        org1_admin = get_peer_org_admin(client, 'org1')
        org1_tx_context = TXContext(org1_admin, Ecies())
        client.tx_context = org1_tx_context
        org1_admin_signature = client.sign_channel_config(config)
        org1_admin_signature_bytes = \
            org1_admin_signature.SerializeToString()

        signatures.append(org1_admin_signature_bytes)

        org2_admin = get_peer_org_admin(client, 'org2')
        org2_tx_context = TXContext(org2_admin, Ecies())
        client.tx_context = org2_tx_context
        org2_admin_signature = client.sign_channel_config(config)
        org2_admin_signature_bytes = \
            org2_admin_signature.SerializeToString()
        signatures.append(org2_admin_signature_bytes)

        request = {'config': config,
                   'signatures': signatures,
                   'channel_name': self.channel_name,
                   'orderer': orderer,
                   'tx_id': tx_id,
                   'nonce': nonce}
        response = client.create_channel(request)

        def on_next(x):
            status, _ = x
            self.assertEqual(status.status, 200)

        def on_error(x):
            assert(False)

        def on_completed():
            assert(True)

        response.subscribe(on_next, on_error, on_completed)


if __name__ == "__main__":
    unittest.main()
