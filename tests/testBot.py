import unittest

import sys
sys.path.append("app")
import algorithm.model as model
import algorithm.function as fun

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
        gensSize = 5
        bot = model.Bot.create(fun.polymon, gensSize)

        # Test mutation 100000 times
        for p in range(0, 10000):
            origGens = bot._gens.copy()
            bot.mutate()
            self.assertEqual(len(origGens), len(bot._gens), "Bot's gens size must not be changed")
            mutatedIndexes = []
            for i in range(0, len(origGens)):
                if origGens[i] != bot._gens[i]:
                    mutatedIndexes.append(i)
            self.assertEqual(1, len(mutatedIndexes), "Only one index must be mutated")
            origValue = origGens[mutatedIndexes[0]]
            newValue = bot._gens[mutatedIndexes[0]]
            deviation = abs((newValue - origValue) / origValue)
            self.assertTrue(deviation <= 1.0, "Incorrect mutation")

    
if __name__ == '__main__':
    unittest.main()
