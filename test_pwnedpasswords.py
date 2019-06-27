#!/usr/bin/env python3

import unittest
import hashlib
from . import pwnedpasswords

class TestPwnedPasswords(unittest.TestCase):
    def setUp(self):
        self.value = "123123"
        self.num_matches = 2194818
        self.password = pwnedpasswords.Password(self.value)

    def test_check(self):
        self.assertEqual(self.password.check(), self.num_matches)

    def test_range(self):
        sha = "601F1889667EFAEBB33B8C12572835DA3F027F78"
        result = self.password.range().get(sha[5:])
        self.assertEqual(result, self.num_matches)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPwnedPasswords)
    unittest.TextTestRunner(verbosity=2).run(suite)

