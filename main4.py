import unittest
import math as mt


class Triga():
    ##Значения будут передаваться в радианах
    def calculate(self, val: float, pers: int):
        sin_, cos_ = round(mt.sin(val), pers), round(mt.cos(val), pers)
        tg_, ctg_ = "Не вычисляется", "Не вычисляется"

        if cos_:
            tg_ = round(sin_ / cos_, pers)

        if sin_:
            ctg_ = round(cos_ / sin_, pers)

        return (sin_, cos_, tg_, ctg_)


class TestTriga(unittest.TestCase):
    def setUp(self):
        self.triga = Triga()

    def test_zero(self):
        self.assertEqual(self.triga.calculate(0, 1), (0.0, 1.0, 0.0, "Не вычисляется"))

    def test_ninety(self):
        self.assertEqual(self.triga.calculate(mt.pi / 2, 1), (1.0, 0.0, "Не вычисляется", 0.0))

    def test_fourty_five(self):
        self.assertEqual(self.triga.calculate(mt.pi / 4, 1), (round(mt.sqrt(2) / 2, 1), round(mt.sqrt(2) / 2, 1), 1.0, 1.0))


if __name__ == "__main__":
  unittest.main()