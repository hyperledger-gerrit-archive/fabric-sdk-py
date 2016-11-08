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

import hfs.api.connection as conn


class ConnectionTest(unittest.TestCase):
    """Test for API connection module. """

    def setUp(self):
        self.address = 'http://fake-url.org'
        self.port = 1234

    def test_init(self):
        """Test case for initializing the Connection Object."""
        conn = conn.Connection(self.address, self.port)
        self.assertEqual(conn.address, self.address)
        self.assertEqual(conn.port, self.port)

        conn = conn.Connection("127.0.0.1", 9876)
        self.assertEqual(conn.address, "127.0.0.1")
        self.assertEqual(conn.port, 9876)

        conn = conn.Connection(certificate=self.certificate,
                          ssl_target_name_override="tca",
                          default_authority="tca")
        conn.address = self.address
        self.assertEqual(conn.address, self.address)
        self.assertEqual(conn.certificate, self.certificate)
        self.assertEqual(conn.ssl_target_name_override, 'tca')
        self.assertEqual(conn.default_authority, 'tca')


if __name__ == '__main__':
    unittest.main()
