import unittest
from sub import sub

class TestSubMethods(unittest.TestCase):

    def test_sub(self):
        self.assertEquals(sub(2,1), 1)


if __name__ == "__main__":
    unittest.main()
