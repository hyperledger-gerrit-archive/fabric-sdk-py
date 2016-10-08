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
import os
from abc import ABCMeta, abstractmethod

import six
import hashlib

import sys
from ecdsa import SigningKey, NIST256p, NIST384p

if sys.version_info < (3, 6):
    import sha3


DEFAULT_NONCE_SIZE = 24

CURVE_P_256_Size = 256
CURVE_P_384_Size = 384

SHA2 = "SHA2"
SHA3 = "SHA3"


@six.add_metaclass(ABCMeta)
class Crypto(object):
    """
    An abstract base class for crypto.
    """

    @abstractmethod
    def generate_key_pair(self):
        """
        Generate asymmetric key pair.
        :return: An object including private and public keys
        """

    @abstractmethod
    def decrypt(self, private_key, cipher_text):
        """
        Decrypt the cipher text by encryption private key.
        :param private_key: Encryption private key
        :param cipher_text: Cipher text received
        :return: An object including secure context
        """

    @abstractmethod
    def sign(self, private_key, message):
        """
        Sign the origin message by signing private key.
        :param private_key: Signing private key
        :param message: Origin message
        :return: An object including secure context
        """


def generate_nonce(size):
    """
    Generate a secure random for cryptographic use.
    :param size: Number of bytes
    :return: Secure random bytes
    """
    return os.urandom(size)


class Ecies(Crypto):
    """
    A crypto implementation based on ECDSA and SHA.
    """

    def __init__(self, security_level, hash_algorithm):
        if security_level == CURVE_P_256_Size:
            self.curve = NIST256p
        else:
            self.curve = NIST384p

        if hash_algorithm == SHA2:
            self.hash = hashlib.sha256
        elif hash_algorithm == SHA3 and security_level == CURVE_P_256_Size:
            self.hash = hashlib.sha3_256()
        else:
            self.hash = hashlib.sha3_384()

    def sign(self, private_key, message):
        pass

    def generate_key_pair(self):
        return ECC.generate(curve=self.curve)

    def decrypt(self, private_key, cipher_text):
        pass
