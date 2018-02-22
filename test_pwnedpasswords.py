#!/usr/bin/env python3

import unittest

class TestPwnedPasswords(unittest.TestCase):
    def setUp(self):
        pass

    def test_example(self):
        assert(2 + 2 == 4)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPwnedPasswords)
    unittest.TextTestRunner(verbosity=2).run(suite)

