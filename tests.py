"""Unit tests for pycdm"""

import unittest

import pyhulu

DEVICE_CODE = '159'
DEVICE_KEY = bytes.fromhex('6ebfc84f3c304217b20fd9a66cb5957f')


class ClientTests(unittest.TestCase):
    """
    ClientTests()

    Test cases for the client module
    """

    def setUp(self):
        self.client = pyhulu.HuluClient(
            device_code=DEVICE_CODE,
            device_key=DEVICE_KEY,
            cookies=None
        )

    def test_load_playlist(self):
        """
        test_load_playlist()

        Tests playlist loading
        """

        playlist = self.client.load_playlist(60873890)
        self.assertIsInstance(playlist, dict)

    def test_exception(self):
        """
        test_exception()

        Tests exception raising
        """

        self.assertRaises(ValueError, self.client.load_playlist, 0)


class DeviceTests(unittest.TestCase):
    """
    DeviceTests()

    Test cases for the device module
    """

    def test_exceptions(self):
        """
        test_exceptions()

        Tests exception raising
        """

        self.assertRaises(ValueError, pyhulu.device.Device, 0, DEVICE_KEY)
        self.assertRaises(ValueError, pyhulu.device.Device, DEVICE_CODE, b'\0')


if __name__ == '__main__':
    unittest.main()
