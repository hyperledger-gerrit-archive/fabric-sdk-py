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
import base64
import json

import requests
import rx


class COPClient(object):
    """Client for communicating with the Fabric COP APIs."""

    def __init__(self, target, ca_certs_path=None):
        """ Init COP client.

        Args:
            target: COP server address including protocol,hostname,port
            ca_certs_path: Local ca certs path
        """
        self._ca_certs_path = ca_certs_path
        self._base_url = target + "/api/v1/cfssl/"

    def enroll(self, enrollment_id, enrollment_secret, csr):
        """Enroll a registered user in order to receive a signed X509 certificate

        Args:
            enrollment_id: The registered ID to use for enrollment
            enrollment_secret: The secret associated with the enrollment ID
            csr: PEM-encoded PKCS#10 certificate signing request

        Returns:
            A rx.Observable object of belows
                success:
                    PEM-encoded X509 certificate
                failed:
                    HTTPError: Http invoke exception
                    ValueError: Failed response, json parse error, args missing

        """
        if not enrollment_id or not enrollment_secret or not csr:
            rx.Observable.just(ValueError(
                    "Missing required parameters. "
                    "'enrollmentID', 'enrollmentSecret' and 'csr' are all required."))

        rx.Observable.start(lambda: self._enroll_callable(enrollment_id, enrollment_secret, csr))

    def _enroll_callable(self, enrollment_id, enrollment_secret, csr):
        """Actual enrollment action.

        Args:
            enrollment_id: The registered ID to use for enrollment
            enrollment_secret: The secret associated with the enrollment ID
            csr: PEM-encoded PKCS#10 certificate signing request

        Returns: PEM-encoded X509 certificate

        Raises:
            HTTPError: Http invoke exception
            ValueError: Failed response, json parse error, args missing
        """
        response = requests.post(self._base_url + "enroll", data=csr,
                                 auth=(enrollment_id, enrollment_secret),
                                 verify=self._ca_certs_path)

        enrollment_response = json.loads(response.json())
        if enrollment_response.success:
            return base64.b64decode(enrollment_response.result)
        else:
            raise ValueError("Enrollment failed with errors {0}".format(enrollment_response.errors))
