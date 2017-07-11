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

from hfc.protos.peer import chaincode_pb2


class TXProposalRequest(object):
    """ Class represents transaction proposal request."""

    def __init__(self, user_context=None, cc_path=None,
                 cc_name=None, cc_version=None, fcn=None,
                 cc_endorsement_policy=None, proposal_wait_time=-1,
                 transient_map=None, packaged_cc=None):
        """ Construct transaction proposal request"""
        self._user_context = user_context
        self._submitted = False
        self._cc_path = cc_path
        self._cc_name = cc_name
        self._cc_version = cc_version
        self._fcn = fcn
        self._cc_lang = chaincode_pb2.ChaincodeSpec.Type.Value('GOLANG')
        self._cc_endorsement_policy = cc_endorsement_policy
        self._proposal_wait_time = proposal_wait_time
        if transient_map is None:
            self._transient_map = {}
        else:
            self._transient_map = transient_map
        self._packaged_cc = packaged_cc

    @property
    def user_context(self):
        """Get user context"""
        return self._user_context

    @user_context.setter
    def user_context(self, user_context):
        """Set user context"""
        self._user_context = user_context

    @property
    def proposal_wait_time(self):
        """Get proposal wait time"""
        return self._proposal_wait_time

    @proposal_wait_time.setter
    def proposal_wait_time(self, proposal_wait_time):
        """Set proposal wait time
        
        Args:
            proposal_wait_time: proposal wait time

        """
        self._proposal_wait_time = proposal_wait_time
