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
from hfc.fabric import user, transaction
from hfc.fabric.transaction import tx_proposal_request
from hfc.util.utils import create_serialized_identity


class TXContext(object):
    """ A class represent Transaction context."""

    def __init__(self, user, crypto, tx_prop_req, prop_wait_time=-1):
        """ Construct transaction context

        Args:
            prop_wait_time (int): proposal request wait timeout 
            tx_prop_req (object): transaction proposal request  
            user: user
            crypto: crypto
        """
        self._tx_prop_req = tx_prop_req
        self._user = user
        self._crypto = crypto
        self._identity = create_serialized_identity(user)
        self._nonce = crypto.generate_nonce(24)
        hash_func = crypto.hash
        self._tx_id = hash_func(self._nonce + self._identity).hexdigest()
        self._prop_wait_time = prop_wait_time

    @property
    def tx_id(self):
        """ Get transaction id."""
        return self._tx_id

    @property
    def epoch(self):
        """ Get epoch."""
        return 0

    @property
    def nonce(self):
        """ Get nonce"""
        return self._nonce

    @property
    def identity(self):
        """Get identity"""
        return self._identity

    def sign(self, plain_text):
        """Sign the text"""
        return self._crypto.sign(self._user.enrollment.private_key,
                                 plain_text)

    @property
    def prop_wait_time(self):
        """Get proposal wait time"""
        return self._prop_wait_time

    @prop_wait_time.setter
    def prop_wait_time(self, proposal_wait_time):
        """Set proposal wait time"""
        self._prop_wait_time = proposal_wait_time

    @property
    def tx_prop_req(self):
        """Get transaction proposal request"""
        return self._tx_prop_req

    @tx_prop_req.setter
    def tx_prop_req(self, tx_prop_req):
        """Set transaction proposal request"""
        self._tx_prop_req = tx_prop_req

    @property
    def user(self):
        """Get request user"""
        return self._user

    @property
    def crypto(self):
        """Get """
        return self._crypto


def validate(tx_context):
    """Validate transaction context
    
    Args:
        tx_context: transaction context
 
    Returns: transaction context if no error

    Raises:
            ValueError: Invalid transaction context
 
    """
    if not tx_context:
        raise ValueError("Missing transaction context object")

    if not tx_context.crypto:
        raise ValueError("Missing 'crypto' parameter "
                         "in the transaction context object")

    if not tx_context.user:
        raise ValueError("Missing 'user' parameter "
                         "in the transaction context object")

    if not tx_context.tx_prop_req:
        raise ValueError("Missing 'tx_prop_req' parameter "
                         "in the transaction context object")


def create_tx_context(user, crypto, tx_prop_req, prop_wait_time=-1):
    """Create transaction context
    
    Args:
        tx_prop_req: transaction proposal request
        user: user
        crypto: crypto
        prop_wait_time: proposal wait time 

    Returns: a transaction context instance

    """
    tx_context = TXContext(user, crypto, tx_prop_req, prop_wait_time)
    return validate(tx_context)
