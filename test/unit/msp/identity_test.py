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

import unittest

from hfc.fabric.msp.identity import Identity
from hfc.fabric.msp.msp import MSP


class IdentityTest(unittest.TestCase):

    def test_create_identity(self):

        msp = MSP('org1msp')
        identity = Identity('org1_msp', 'cert', 'public_key', msp)
        self.assertTrue(isinstance(identity, Identity))


if __name__ == '__main__':
    unittest.main()