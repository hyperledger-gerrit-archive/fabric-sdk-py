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
import unittest

from hfs.api.crypto.crypto import CURVE_P_256_Size, Ecies, SHA3, CURVE_P_384_Size


class CryptoTest(unittest.TestCase):
    def testEciesEncrypt(self):
        ecies384 = Ecies(CURVE_P_384_Size, SHA3)
        peer_private_key = ecies384.generate_private_key()
        plain_text = "Hello world!"
        assert len(ecies384.encrypt(peer_private_key.public_key(), plain_text)) == 196

        ecies256 = Ecies(CURVE_P_256_Size, SHA3)
        peer_private_key1 = ecies256.generate_private_key()
        plain_text1 = "Hello world!"
        assert len(ecies256.encrypt(peer_private_key1.public_key(), plain_text1)) == 151
