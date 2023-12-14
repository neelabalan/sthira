import unittest
from sthira import Constant
from sthira import constant
from sthira import InstanceCreationError
from sthira import dispatch


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

    def test_inheritance(self):
        class Bird(metaclass=Constant):
            BEAK = "Beak"
            FEATHERS = "Feathers"
            WORD = "Bird is the word"

        class Crow(Bird):
            WORD = "Caww!"
            NEW_FEATURE = "Smart"

        self.assertEqual(Bird.WORD, "Bird is the word")
        self.assertEqual(Crow.WORD, "Caww!")
        self.assertEqual(Crow.NEW_FEATURE, "Smart")

        with self.assertRaises(AttributeError):
            Bird.WORD = "change?"

        with self.assertRaises(AttributeError):
            Crow.WORD = "change?"

        with self.assertRaises(AttributeError):
            Crow.NEW_FEATURE = "change?"


@constant
class Red:
    BRICK = "#AA4A44"
    CADMIUM = "##D22B2B"


@constant
class Green:
    LIME = "#32CD32"
    LIGHT = "#90EE90"


@constant
class Color:
    RED = Red
    GREEN = Green
    YELLOW = "not_there_yet"


class TestDispatched(unittest.TestCase):
    def test_dispatched(self):
        @dispatch
        def get_color(color, input_):
            # Default implementation
            raise NotImplementedError("Unsupported color!")

        @get_color.register(Color.RED)
        def _(input_):
            return "I'm red"

        @get_color.register(Color.GREEN)
        def _(input_):
            return "hulk out"

        # Test default implementation
        with self.assertRaises(NotImplementedError):
            get_color(Color.YELLOW, "input")

        # Test registered implementations
        self.assertEqual(get_color(Color.GREEN, "input"), "hulk out")
        self.assertEqual(get_color(Color.RED, "input"), "I'm red")


if __name__ == "__main__":
    unittest.main()
