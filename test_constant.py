import unittest
from sthira import Constant
from sthira import InstanceCreationError

class TestConstant(unittest.TestCase):
    def test_init(self):
        class Color(metaclass=Constant):
            RED = 0
            GREEN = 1
            BLUE = 2

        with self.assertRaises(InstanceCreationError):
            Color()

    def test_setattr(self):
        class Color(metaclass=Constant):
            RED = 0
            GREEN = 1
            BLUE = 2

        with self.assertRaises(AttributeError):
            Color.RED = 1

    def test_str_repr(self):
        class Color(metaclass=Constant):
            RED = 0
            GREEN = 1
            BLUE = 2

        self.assertEqual(str(Color), "Color")
        self.assertEqual(repr(Color), "Color")

if __name__ == "__main__":
    unittest.main()
