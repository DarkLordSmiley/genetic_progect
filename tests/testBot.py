import unittest

import sys
sys.path.append("app")
import algorithm.model as model

class TestBot(unittest.TestCase):
    def testCreation(self):
        def testFun(x, gens):
            m = map(lambda val: val * x, gens)
            return sum(list(m))
        gensSize = 5
        bot = model.Bot.create(testFun, gensSize)
        self.assertIsNotNone(bot, "Bot must be created and initialized")
        self.assertIsNotNone(bot._gens, "Bot's gens must be initialized")
        self.assertIsNotNone(bot._solveFunction, "Bot's solve function must be initialized")
        self.assertEqual(len(bot._gens), gensSize, "Bot's gens size is not valid")
        self.assertEqual(bot._solveFunction, testFun, "Bot's solve function is not valid")

        expectedValues = [testFun(54, bot._gens), testFun(56, bot._gens)]
        actualValues = bot.calculate([54, 56])
        self.assertListEqual(expectedValues, actualValues, "Calculation is not correct")

    def testMutation(self):
        self.assertTrue(True)
    
if __name__ == '__main__':
    unittest.main()
