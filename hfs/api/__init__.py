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


class ApiBase(object):
    """ Base object - Used in nodes and peers in the network.

    It has a specific Grpc channel address.
    """

    def __init__(self,
                 address,
                 certificate=None,
                 ssl_target_name_override=None,
                 default_authority=None):
        self.logger = logging.getLogger(__name__)
        if certificate:
            self.certificate = certificate
        if ssl_target_name_override:
            self.ssl_target_name_override = 'tlsca'
        if default_authority:
            self.default_authority = 'tlsca'

        self.address = address

    def getAddress(self):
        """
          Get the Address of the node/peer.
          @returns {string} Get the address associated with the Node/peer.
        """
        return self.address
