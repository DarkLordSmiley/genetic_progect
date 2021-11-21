import unittest

import sys
sys.path.append("app")
import algorithm.function as fun

class TestPolynom(unittest.TestCase):
    def testPolynom1(self):
        testFun = lambda x: 2.1 + x * 3.2
        gens = [2.1, 3.2]
        for i in range(0, 200):
            x = (float(i) -100.0) / 10
            expected = testFun(x)
            self.assertAlmostEqual(fun.polymon(x, gens), expected, 5, "Неверное значение polynom функции")

    def testPolynom2(self):
        testFun = lambda x: 2.1 + x * 3.2 - x**2 * 25.0 
        gens = [2.1, 3.2, -25.0]
        for i in range(0, 200):
            x = (float(i) -100.0) / 10
            expected = testFun(x)
            self.assertAlmostEqual(fun.polymon(x, gens), expected, 5, "Неверное значение polynom функции")

if __name__ == '__main__':
    unittest.main()
