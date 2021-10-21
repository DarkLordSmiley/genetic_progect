import numpy as np
import config

def getSquareError(errors):
    return np.square(errors).mean()

class Bot:
    """
    Бот - это организм, содержащий хромосому, т.е. набор генов для решения задачи.
    Бот так же содержит ссылку на Solve функцию, которую применяет к своим хромосомам
    для нахождения Аллели - решения данного организма. Это решение может использоваться
    для оценки приспособленности данного организма
    """

    def __init__(self, solveFunction, chromosomeSize: int):
        """
        Конструктор с Solve функцией и размером хромосомы - т.е. кол-вом ген.
        """
        self._solveFunction = solveFunction
        self._gens = self._initGens(chromosomeSize)

    def _initGens(self, chromosomeSize: int):
        """
        Создает массив ген указанного в chromosomeSize размера и инициализирует его
        случайными значениями float
        """

        return np.random.uniform(-100.0, 100.0, chromosomeSize)

    #ToDo        

class Population:
    """
    Класс-контейнер, содержащий популяцию ботов среди которых проводит отбор на основе
    функции приспособления (стоимости), выбирая особей с минимальным значением функции
    стоимости.
    """

    def __init__(self, costFunction, bots):
        """
        Конструктор с cost функцией и коллекцией ботов.
        """
        self._costFunction = costFunction
        self.bots = bots
        self._generation = 0

    def getGeneration(self):
        return self._generation
    
    def selectBestAndGenerate(self, trainMatrix, numberOfBest):
        """
        Выбираем лучшего представителя (с минимальной ошибкой - значением cost функции) и
        генерируем новое поколение из лучших
        """

        estimations = self._collectEstimations(trainMatrix)

        bestBot = self._findBest(estimations)

        # Gene// Reproduce new population from the given best species
        for (int i = 0; i < size; i++) {
            IBot parent1 = bestBots.get(RandomUtils.nextInt(0, bestBotsSize));
            IBot parent2 = bestBots.get(RandomUtils.nextInt(0, bestBotsSize));
            IBot child = parent1.reproduce(parent2);
            child.mutate();
            bots.set(i, child);
        }

        // Increase generation
        generation++;

        // Return errors of the best bots
        return bestEstimations.stream().mapToDouble(BotEstimation::getError).toArray()
    
    def _collectEstimations(self, trainMatrix):
        # ToDo
        pass

    def _findBest(selt, estimations):
        best = estimations[0]
        for estimation in estimations:
            if best.error > estimation.error:
                best = estimation
        return best

class Estimation:
    """
    Class container which is used to hold bot and its error.
    """

    def __init__(self, bot, errors):
        self.bot = bot
        self.error = getSquareError(errors)
    