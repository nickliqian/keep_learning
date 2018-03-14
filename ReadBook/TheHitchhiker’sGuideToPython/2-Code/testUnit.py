import unittest

def func(x):
    return x + 1

class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(func(3), 5)
