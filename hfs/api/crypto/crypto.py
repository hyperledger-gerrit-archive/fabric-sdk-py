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
import hashlib
import hmac
import sys
from abc import ABCMeta, abstractmethod

import six
from Cryptodome import Random
from Cryptodome.Cipher import AES
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from hkdf import Hkdf

if sys.version_info < (3, 6):
    import sha3

DEFAULT_NONCE_SIZE = 24

CURVE_P_256_Size = 256
CURVE_P_384_Size = 384

SHA2 = "SHA2"
SHA3 = "SHA3"

AES_KEY_LENGTH = 32
HMAC_KEY_LENGTH = 32
IV_LENGTH = 16


@six.add_metaclass(ABCMeta)
class Crypto(object):
    """ An abstract base class for crypto. """

    @abstractmethod
    def generate_private_key(self):
        """ Generate asymmetric key pair.

        :return: An private key object which include public key object.
        """

    @abstractmethod
    def encrypt(self, public_key, message):
        """ Encrypt the message by encryption public key.

        :param public_key: Encryption public key
        :param message: message need encrypt

        :return: An object including secure context
        """

    @abstractmethod
    def decrypt(self, private_key, cipher_text):
        """ Decrypt the cipher text by encryption private key.

        :param private_key: Encryption private key
        :param cipher_text: Cipher text received

        :return: An object including secure context
        """

    @abstractmethod
    def sign(self, private_key, message):
        """ Sign the origin message by signing private key.

        :param private_key: Signing private key
        :param message: Origin message

        :return: An object including secure context
        """


def generate_nonce(size):
    """ Generate a secure random for cryptographic use.

    :param size: Number of bytes

    :return: Secure random bytes
    """
    return Random.get_random_bytes(size)


class Ecies(Crypto):
    """ A crypto implementation based on ECDSA and SHA. """

    def __init__(self, security_level, hash_algorithm):
        """ Init curve and hash function.

        :param security_level: security level
        :param hash_algorithm: hash function
        """
        if security_level == CURVE_P_256_Size:
            self.curve = ec.SECP256R1
        else:
            self.curve = ec.SECP384R1

        if hash_algorithm == SHA2:
            self.hash = hashlib.sha256
        elif hash_algorithm == SHA3 and security_level == CURVE_P_256_Size:
            self.hash = hashlib.sha3_256
        else:
            self.hash = hashlib.sha3_384

    def sign(self, private_key, message):
        pass

    def generate_private_key(self):
        """ECDSA key pair generation by current curve.

        :return: A private key object which include public key object.
        """
        return ec.generate_private_key(self.curve, default_backend())

    def decrypt(self, private_key, cipher_text):
        pass

    def encrypt(self, public_key, plain_text):
        """Ecies encrypt plain text.

        First create a ephemeral ecdsa key pair, then serialize the public key for part of result.
        Then derived a shared key based ecdh, using the key based hkdf to generate aes key and hmac key,
        using aes-256-cfb to generate the part of result.
        Last using hmac-sha3 and the part of previous step to generate last part of result.

        :param public_key: public key from peer party
        :param plain_text: plain text
        :return:
        """
        ephemeral_private_key = self.generate_private_key()
        Rb = ephemeral_private_key.public_key().public_bytes(encoding=Encoding.DER,
                                                             format=PublicFormat.SubjectPublicKeyInfo)
        Z = ephemeral_private_key.exchange(ec.ECDH(), public_key)

        hkdf_output = Hkdf(salt=None, input_key_material=Z, hash=self.hash).expand(
                length=AES_KEY_LENGTH + HMAC_KEY_LENGTH)
        aes_key = hkdf_output[:AES_KEY_LENGTH]
        hmac_key = hkdf_output[AES_KEY_LENGTH:AES_KEY_LENGTH + HMAC_KEY_LENGTH]

        aes_cipher = AES.new(aes_key, AES.MODE_CFB)
        EM = aes_cipher.iv + aes_cipher.encrypt(plain_text)

        mac = hmac.HMAC(hmac_key, EM, self.hash)
        mac.update(EM)
        D = mac.digest()

        return Rb + EM + D
