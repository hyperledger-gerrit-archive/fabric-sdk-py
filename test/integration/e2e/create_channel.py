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

from hfc.fabrci.client import Client
from hfc.fabric.order import Orderer
from hfc.fabric.util import file_key_value_store

from test.unit import cli_call
from . import util

_logger = logging.getLogger(__file__ + "e2e test")


class CreateChannelTest(unittest.TestCase):

    def setUp(self):

        self.base_path = "/tmp/fabric-sdk-py"
        self.kv_store_path = os.path.join(self.base_path, "key-value-store")
        self.compose_file_path = os.path.normpath(
            os.path.join(util.pwd, "../../fixtures/docker-compose-base.yaml"))

        self.start_test_env()

    def tearDown(self):

        self.shutdown_test_env()

    def start_test_env(self):

        cli_call(["docker-compose", "-f", self.compose_file_path, "up", "-d"])

    def shutdown_test_env(self):

        cli_call(["docker-compose", "-f", self.compose_file_path, "down"])

    def test_create_channel(self):

        config = None
        channel_name = "channel"
        signatures = []
        client = Client()

        # create the new orderer from the config
        caroot_path = util.orgs.orderer.tls_cacerts
        pem = open(caroot_path).read()
        orderer = Orderer(pem, endmpoint=util.orgs.orderer.url,
                          opts={"hostname": util.orgs.orderer.username})

        # set the state_store
        client.state_store = file_key_value_store(self.kv_store_path)

        # enroll the users and sign the config

        envelope = util.users.orderer.envelope
        ret = util.get_orderer_admin(client)
        if ret:
            orderer_admin = ret
            envelope_byte = open(envelope).read()
            config = client.extract_channel_config(envelope_byte)
        client.user_context = None

        ret = util.get_submitter(client, True, "org1")
        if ret:
            signature = client.sign_channel_config(config)
            signatures.append(signature)
        client.user_context = None

        ret = util.get_submitter(client, True, "org2")
        if ret:
            signature = client.sign_channel_config(config)
            signatures.append(signature)
        client.user_context = None

        client.user_context = orderer_admin
        signature = client.sign_channel_config(config)
        signatures.append(signature)

        nonce = util.get_nonce()
        tx_id = client.build_trasaction_id(nonce)

        # buidl the request and create the channel
        request = {}
        request['config'] = config
        request['signatures'] = signatures
        request['channel_name'] = channel_name
        request['orderer'] = orderer
        request['tx_id'] = tx_id

        ret = client.create_channel(request)
        self.assertTrue(ret)


if __name__ == "__main__":
    unittest.main()
