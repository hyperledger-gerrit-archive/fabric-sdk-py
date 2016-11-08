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

from hfs.api import ApiBase


class ApiBaseTest(unittest.TestCase):
    """Test for API base module. """

    def setUp(self):
        self.certificate = b'Hello world-some certificate info'
        self.address = b'http://fake-url.org'

    def test_init(self):
        """Test case for initializing the Base Object."""
        base = ApiBase(self.address)
        self.assertEqual(base.address, self.address)

        base = ApiBase(self.address, certificate=self.certificate)
        self.assertEqual(base.address, self.address)
        self.assertEqual(base.certificate, self.certificate)

        base = ApiBase(self.address, ssl_target_name_override=True)
        self.assertEqual(base.address, self.address)
        self.assertEqual(base.ssl_target_name_override, 'tlsca')

        base = ApiBase(self.address,
                       certificate=self.certificate,
                       ssl_target_name_override=True)
        self.assertEqual(base.address, self.address)
        self.assertEqual(base.certificate, self.certificate)
        self.assertEqual(base.ssl_target_name_override, 'tlsca')

        base = ApiBase(self.address,
                       certificate=self.certificate,
                       ssl_target_name_override=True,
                       default_authority=True)
        self.assertEqual(base.address, self.address)
        self.assertEqual(base.certificate, self.certificate)
        self.assertEqual(base.ssl_target_name_override, 'tlsca')
        self.assertEqual(base.default_authority, 'tlsca')

    def test_getAddress(self):
        """Test case for security level 384, hash SHA3."""
        base = ApiBase(self.address, certificate=self.certificate)
        self.assertEqual(base.getAddress(), self.address)
        base = ApiBase("http://myurl.com",
                       certificate=self.certificate,
                       ssl_target_name_override=True)
        self.assertEqual(base.getAddress(), "http://myurl.com")


if __name__ == '__main__':
    unittest.main()
