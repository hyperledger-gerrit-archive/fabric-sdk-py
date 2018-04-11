"""
# Copyright IBM Corp. 2017 All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""


import unittest
import logging
import sys
import time

from hfc.fabric.client import Client
from hfc.util.keyvaluestore import FileKeyValueStore

from test.integration.utils import cli_call, BaseTestCase
from test.integration.config import E2E_CONFIG
from test.integration.e2e_utils import build_channel_request, \
    build_join_channel_req

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
test_network = E2E_CONFIG['test-network']

if sys.version_info < (3, 0):
    from Queue import Queue
else:
    from queue import Queue


class E2eTest(BaseTestCase):

    def setUp(self):
        super(E2eTest, self).setUp()

    def tearDown(self):
        super(E2eTest, self).tearDown()

    def channel_create(self):
        logger.info("E2E: Channel creation start: name={}".format(
            self.channel_name))

        # By default, self.user is the admin of org1
        response = self.client.channel_create('orderer.example.com',
                                              self.channel_name,
                                              self.user,
                                              self.channel_tx)
        self.assertTrue(response)

        logger.info("E2E: Channel creation done: name={}".format(
            self.channel_name))

    def channel_join(self):
        # wait for channel created
        time.sleep(5)

        logger.info("E2E: Channel join start: name={}".format(
            self.channel_name))
        # channel must already exist when to join
        channel = self.client.get_channel(self.channel_name)
        self.assertIsNotNone(channel)

        response = self.client.channel_join(self.channel_name,
                                            ['peer0.org1.example.com'],
                                            'orderer.example.com')
        self.assertTrue(response)
        logger.info("E2E: Channel join done: name={}".format(
            self.channel_name))

    def channel_join2(self):

        # wait for channel created
        time.sleep(10)

        # channel must already exist when to join
        channel = self.client.get_channel(self.channel_name)
        self.assertIsNotNone(channel)

        logger.info("start to join channel")
        orgs = ["org1.example.com", "org2.example.com"]
        done = True
        for org in orgs:
            request = build_join_channel_req(org, channel, self.client)
            done = done and channel.join_channel(request)
            if done:
                logger.info("peers in org: %s join channel: %s.",
                            org, self.channel_name)
        if done:
            logger.info("joining channel tested successfully.")
        assert(done)

    def install_chaincode(self):

        pass

    def install_chaincode_fail(self):

        pass

    def instantiate_chaincode(self):

        pass

    def invoke_transaction(self):

        pass

    def query(self):

        pass

    def test_in_sequence(self):

        self.channel_create()
        self.channel_join2()
        self.install_chaincode()
        self.install_chaincode_fail()
        self.instantiate_chaincode()
        self.invoke_transaction()
        self.query()


if __name__ == "__main__":
    unittest.main()
