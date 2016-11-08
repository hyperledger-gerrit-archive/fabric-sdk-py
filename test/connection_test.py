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

from hfs.api.connection import Connection


class ConnectionTest(unittest.TestCase):
    """Test for API connection module. """

    def setUp(self):
        self.certificate = b'Hello world-some certificate info'
        self.address = b'http://fake-url.org'

    def test_init(self):
        """Test case for initializing the Connection Object."""
        conn = Connection()
        conn._address = self.address
        self.assertEqual(conn._address, self.address)
        self.assertEqual(conn.ssl_target_name_override, 'tlsca')

        conn = Connection(certificate=self.certificate)
        conn._address = self.address
        self.assertEqual(conn._address, self.address)
        self.assertEqual(conn.certificate, self.certificate)
        self.assertEqual(conn.ssl_target_name_override, 'tlsca')

        conn = Connection(ssl_target_name_override="eca")
        conn._address = self.address
        self.assertEqual(conn._address, self.address)
        self.assertEqual(conn.ssl_target_name_override, 'eca')

        conn = Connection(certificate=self.certificate,
                          ssl_target_name_override="aca")
        conn._address = self.address
        self.assertEqual(conn._address, self.address)
        self.assertEqual(conn.certificate, self.certificate)
        self.assertEqual(conn.ssl_target_name_override, 'aca')

        conn = Connection(certificate=self.certificate,
                          ssl_target_name_override="tca",
                          default_authority="tca")
        conn._address = self.address
        self.assertEqual(conn._address, self.address)
        self.assertEqual(conn.certificate, self.certificate)
        self.assertEqual(conn.ssl_target_name_override, 'tca')
        self.assertEqual(conn.default_authority, 'tca')


if __name__ == '__main__':
    unittest.main()
