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

    def test_init(self):
        """Test case for initializing the Connection Object."""
        my_conn = conn.Connection(self.address)
        self.assertEqual(my_conn.grpc_addr, self.address)
        self.assertIsNotNone(my_conn.channel)

        my_conn = conn.Connection("127.0.0.1")
        self.assertEqual(my_conn.grpc_addr, "127.0.0.1")
        self.assertIsNotNone(my_conn.channel)

    def test_factory(self):
        """Test case for returning a Connection object."""
        my_conn = conn.get_connection("127.0.0.1")
        self.assertEqual(my_conn.grpc_addr, "127.0.0.1")
        self.assertIsNotNone(my_conn.channel)


if __name__ == '__main__':
    unittest.main()
