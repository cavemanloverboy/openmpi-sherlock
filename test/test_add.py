import unittest
from add import add

class TestAddMethods(unittest.TestCase):


    def test_add(self):
        self.assertEquals(add(2,2), 4)


if __name__ == "__main__":
    unittest.main()
