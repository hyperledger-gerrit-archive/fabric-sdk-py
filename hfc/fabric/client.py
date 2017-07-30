# Copyright arxanfintech.com 2016 All Rights Reserved.
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

import logging

from hfc.fabric.channel.channel import Channel

_logger = logging.getLogger(__name__ + ".client")


class Client(object):
    """
        Main interaction handler with end user.
        Client can maintain several channels.
    """

    def __init__(self):
        """ Construct client"""
        self._channels = {}
        self._crypto_suite = None
        self._user_context = None
        self._state_store = None

    def new_channel(self, name):
        """Init a channel instance with given name.

        :param name: The name of channel

        :return: The inited channel instance

        """
        _logger.debug("New channel with name = {}".format(name))
        if name not in self._channels:
            self._channels[name] = Channel(name, self)
        return self._channels[name]

    def get_channel(self, name):
        """ Get a channel instance

        :param name: the name of the channel

        :return: Get the channel instance with the name or None

        """
        return self._channels.get(name, None)

    @property
    def crypto_suite(self):
        """Get the crypto suite.

        Returns: The crypto_suite instance or None

        """
        return self._crypto_suite

    @crypto_suite.setter
    def crypto_suite(self, crypto_suite):
        """Set the crypto suite to given one.

        Args:
            crypto_suite: The crypto_suite to use.

        Returns: None

        """
        self._crypto_suite = crypto_suite

    @property
    def user_context(self):
        """Get the user context.

        Returns: The user context or None

        """
        return self._user_context

    @user_context.setter
    def user_context(self, user_context):
        """Set the user context to given one.

        Args:
            user_context: The user_context to use.

        Returns: None

        """
        self._user_context = user_context

    @property
    def state_store(self):
        """ Get the KeyValue store.

        Return the keyValue store instance or None

        """
        return self._state_store

    @state_store.setter
    def state_store(self, state_store):
        """ Set the KeyValue store.

        Args:
            state_store: the KeyValue store to use.

        No return Value

        """
        self._state_store = state_store

    def build_transation_id(self, nonce):
        """
        args:
            nonce: random number
        return:
            the transation id of the transaction
        """

        pass

    def sign_channel_config(self, config):
        """
        args:
             config for creating a channel.
        returns:
             the signature
        """

        pass

    def extract_channel_config(self, envelope):
        """
        Desc: extract the protobuf configu pdate object out of
              the config envelope object created by configtxgen tool
        args:
             envelope: encodeed bytes of the config envelop protofu
        return:
             the encoded bytes of the config update protobuf, ready
        to be signed.
        """
        pass

    def create_channel(self, **request):
        """
        args:
            request = {
                      @name(required): channel name
                      @orderer(required): orderer to send the request
                      @signatures(required): signatures from the peers of config
                       it is required when config is used
                      @tx_id(required): transation id for the genesis block
                      @config(optional): extracted from envlope creatted by
                       configtxlator
                  }
        return:
            True if creating channel successfully, False in failure.
        """

        pass
