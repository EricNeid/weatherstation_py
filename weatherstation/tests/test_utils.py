# pylint: skip-file

"""Testing module utils"""
import unittest
import os

from weatherstation.misc import utils


class TestUtils(unittest.TestCase):
    test_data_dir = os.path.abspath("./weatherstation/tests/testdata")
    test_key = os.path.join(test_data_dir, "key.txt")

    def test_read_api_key(self):
        """should return content of api key file"""
        key = utils.read_api_key(self.test_key)

        self.assertEqual("1234567890", key)


if __name__ == '__main__':
    unittest.main()
