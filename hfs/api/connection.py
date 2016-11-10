# Copyright IBM Corp. 2016 All Rights Reserved.
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


class Connection(object):

    def __init__(self,
                 certificate=None,
                 ssl_target_name_override='tlsca',
                 default_authority='tlsca'):
        """ Connection object - Used in nodes and peers in the network.

        Args:
            certificate (obj): (optional) The certificate for the connection
            ssl_target_name_override (str): (optional) The ssl protocol type
            default_authority (str): (optional) The ssl protocol type
        """
        self.logger = logging.getLogger(__name__)

        self._address = None
        self.certificate = certificate
        self.ssl_target_name_override = ssl_target_name_override
        self.default_authority = default_authority

    @property
    def address(self):
        """ Get the Address of the node/peer.
        Args:
            certificate (obj): (optional) The certificate for the connection
            ssl_target_name_override (str): (optional) The ssl protocol type
            default_authority (str): (optional) The ssl protocol type

        Returns:
            str: The address value (<IP address>:<port number>)
        """
        return self._address

    @address.setter
    def address(self, value):
        """ Set the address of the node/peer.
        Args:
            value (str): The address for the connection
            default_authority (str): (optional) The ssl protocol type
        """
        self._address = value
