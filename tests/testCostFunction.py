import unittest

import sys
sys.path.append("app")
import algorithm.function as fun

class TestCost(unittest.TestCase):
    def testCost(self):
        ethalon = 2.0
        value = 2.1
        expected = abs(value - ethalon)
        self.assertAlmostEqual(fun.cost(2.0, 2.1), expected, 5, "Неверное значение cost функции")

    def testCost(self):
        ethalon = -5.0
        value = -4.1
        expected = abs(value - ethalon)
        self.assertAlmostEqual(fun.cost(-5.0, -4.1), expected, 5, "Неверное значение cost функции")
    
if __name__ == '__main__':
    unittest.main()
