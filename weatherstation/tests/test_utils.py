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


class TestFileRingList(unittest.TestCase):
    """Testsuite for class FileRingList"""
    test_data_dir = os.path.abspath("./weatherstation/tests/testdata/fileringlist")
    test_data = [
        os.path.join(test_data_dir, "a.txt"),
        os.path.join(test_data_dir, "b.txt"),
        os.path.join(test_data_dir, "c.txt")
    ]

    unit = None

    def setUp(self):
        self.unit = utils.FileRingList()


    def test_add_directory(self):
        """should contain all files in the directory"""
        self.unit.add_directory(self.test_data_dir)

        self.assertCountEqual(self.test_data, self.unit.fileNames)


    def test_current_and_next(self):
        """should iterate through the loaded files and wrap around"""
        self.unit.add_directory(self.test_data_dir)

        self.assertEqual(self.unit.fileNames[0], self.unit.current())
        self.assertEqual(self.unit.fileNames[1], self.unit.next())
        self.assertEqual(self.unit.fileNames[2], self.unit.next())
        self.assertEqual(self.unit.fileNames[0], self.unit.next())


if __name__ == '__main__':
    unittest.main()
