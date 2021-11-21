import unittest
import math

import sys
sys.path.append("app")
import algorithm.function as fun

class TestSinCos(unittest.TestCase):
    def testSinCos1(self):
        testFun = lambda x: (3.1 + math.sin(x) * 1.2 - math.cos(x) * 4.5 
            - math.sin(2*x) * 0.4 + math.cos(2*x) * 1.8)
        gens = [3.1, 1.2, -0.4, -4.5, 1.8]
        for i in range(0, 200):
            x = (float(i) -100.0) / 10
            expected = testFun(x)
            self.assertAlmostEqual(fun.sinCos(x, gens), expected, 5, "Неверное значение sincos функции")

    def testSinCos2(self):
        testFun = lambda x: (3.1 + math.sin(x) * 1.2 - math.cos(x) * 4.5 
            - math.sin(2*x) * 0.4 + math.cos(2*x) * 1.8 + math.cos(3*x) * 1.3)
        gens = [3.1, 1.2, -0.4, -4.5, 1.8, 1.3]
        for i in range(0, 200):
            x = (float(i) -100.0) / 10
            expected = testFun(x)
            self.assertAlmostEqual(fun.sinCos(x, gens), expected, 5, "Неверное значение sincos функции")

if __name__ == '__main__':
    unittest.main()
