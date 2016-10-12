import unittest
from hfs.util.log import warn


def fun(x):
    return x + 1


class MyTest(unittest.TestCase):
    def test(self):
        warn("MyTest running")
        self.assertEqual(fun(3), 4)
