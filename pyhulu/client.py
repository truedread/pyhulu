"""
Client module

Main module for Hulu API requests
"""

import base64
import binascii
import hashlib
import json
import logging
import random
import requests

from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding

from pyhulu.device import Device


class HuluClient(object):
    """
    HuluClient class

    Main class for Hulu API requests
    """

    def __init__(self, device_code, device_key):
        self.logger = logging.getLogger(__name__)
        self.device = Device(device_code, device_key)

        self.session_key, self.server_key = self.get_session_key()

    def load_playlist(self, video_id) -> dict:
        """
        load_playlist()

        Method to get a playlist containing the MPD
        and license URL for the provided video ID and return it

        @param video_id: String or integer of the video ID
                         to get a playlist for

        @return: Dict of decrypted playlist response
        """

        base_url = 'https://s.hulu.com/playlist'
        params = {
            'video_id': video_id,
            'token': '',
            'device': self.device.device_code,
            'version': '1',
            'device_id': '',
            'kv': self.server_key,
        }

        resp = requests.get(url=base_url, params=params)

        try:
            ciphertext = bytes.fromhex(resp.text)
        except ValueError:
            self.logger.error('Error decoding response hex')
            self.logger.error('Request:')
            for line in json.dumps(params, indent=4).splitlines():
                self.logger.error(line)

            self.logger.error('Response:')
            for line in resp.text.splitlines():
                self.logger.error(line)

            raise ValueError('Error decoding response hex')

        return self.decrypt_response(self.session_key, ciphertext)

    def get_session_key(self) -> bytes:
        """
        get_session_key()

        Method to do a Hulu config request and calculate
        the session key against device key and current server key

        @return: Session key in bytes
        """

        version = '1'
        random_value = random.randrange(1E5, 1E6)

        base = '{device_key},{device},{version},{random_value}'.format(
            device_key=binascii.hexlify(self.device.device_key).decode('utf8'),
            device=self.device.device_code,
            version=version,
            random_value=random_value
        ).encode('utf8')

        nonce = hashlib.md5(base).hexdigest()

        url = 'https://play.hulu.com/config'
        payload = {
            'rv': random_value,
            'mozart_version': '1',
            'region': 'US',
            'version': version,
            'device': self.device.device_code,
            'encrypted_nonce': nonce
        }

        resp = requests.post(url=url, data=payload)

        try:
            ciphertext = bytes.fromhex(resp.text)
        except ValueError:
            self.logger.error('Error decoding response hex')
            self.logger.error('Request:')
            for line in json.dumps(payload, indent=4).splitlines():
                self.logger.error(line)

            self.logger.error('Response:')
            for line in resp.text.splitlines():
                self.logger.error(line)

            raise ValueError('Error decoding response hex')

        config_dict = self.decrypt_response(
            self.device.device_key,
            ciphertext
        )

        derived_key_array = bytearray()
        for device_byte, server_byte in zip(self.device.device_key,
                                            bytes.fromhex(config_dict['key'])):
            derived_key_array.append(device_byte ^ server_byte)

        return bytes(derived_key_array), config_dict['key_id']

    def decrypt_response(self, key, ciphertext) -> dict:
        """
        decrypt_response()

        Method to decrypt an encrypted response with provided key

        @param key: Key in bytes
        @param ciphertext: Ciphertext to decrypt in bytes

        @return: Decrypted response as a dict
        """

        aes_cbc_ctx = AES.new(key, AES.MODE_CBC, iv=b'\0'*16)

        try:
            plaintext = Padding.unpad(aes_cbc_ctx.decrypt(ciphertext), 16)
        except ValueError:
            self.logger.error('Error decrypting response')
            self.logger.error('Ciphertext:')
            self.logger.error(base64.b64encode(ciphertext).decode('utf8'))
            self.logger.error(
                'Tried decrypting with key %s',
                base64.b64encode(key).decode('utf8')
            )

            raise ValueError('Error decrypting response')

        return json.loads(plaintext)

    def __repr__(self):
        return '<HuluClient session_key=%s>' % base64.b64encode(
            self.session_key
        ).decode('utf8')
