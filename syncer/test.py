import unittest

from main import *


class SyncerTest(unittest.TestCase):

    def test_bidon(self):
        self.assertTrue(True)
        
    def test_utile(self):
        self.assertEqual(2, 1 + 1)


if __name__ == '__main__':
    unittest.main()
