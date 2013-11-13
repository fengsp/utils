# -*- coding: utf-8
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import unittest

from signing import Signer


class TestSigner(unittest.TestCase):
    
    def setUp(self):
        self.signer = Signer('fsp')
        self.signature = self.signer.sign('haha')

    def test_unsign(self):
        self.assertEqual(self.signer.unsign(self.signature), 'haha')

    def tearDown(self):
        self.signer = None


if __name__ == '__main__':
    unittest.main()
