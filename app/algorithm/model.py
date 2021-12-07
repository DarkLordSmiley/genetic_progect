import numpy as np
import random
import logging
from multiprocessing import cpu_count, Pool
from functools import partial
import heapq

import time
current_millis = lambda: int(round(time.time() * 1000))

log = logging.getLogger("model")

class Bot:
    """
   Бот - это организм, содержащий хромосому, т.е. набор генов для решения задачи.
   Каждый ген - это коэффициент в модели solve функциях
   Бот так же содержит ссылку на Solve функцию, которую применяет к своим генам
   для нахождения Аллели - решения данного организма. Это решение может использоваться
   для оценки приспособленности данного организма
    """

    def __init__(self, gens, solveFunction):
        """
        Конструктор для создания бота на основе существующего набора ген
        """
        self._gens = gens
        self._solveFunction = solveFunction

    @classmethod
    def create(cls, solveFunction, chromosomeSize: int):
        """
        Статический инициализатор
        """
        gens = Bot._initGens(chromosomeSize)
        return cls(gens, solveFunction)

    @classmethod
    def _initGens(cls, chromosomeSize: int):
        """
        Создает массив ген указанного в chromosomeSize размера и инициализирует его
        случайными значениями float
        """
        return np.random.uniform(-100.0, 100.0, chromosomeSize)

    def calculate(self, inputs):
        """
        Вычисляем значение solve функции на основе значений генов этого
        экземпляра бота
        """
        return self._solveFunction(inputs, self._gens)
        # return list(map(lambda val: self._solveFunction(val, self._gens), inputs))

    def getGens(self):
        return self._gens

    def reproduce(self, partner):
        """
        Генерируем потомка из ген этого бота и переданного. Выбираем гены случайным образом
        """
        if not self._isCompatible(partner):
            raise Exception("Parner bot is not compatible")

        thisBotGenChances = np.random.choice([True, False], size=len(self._gens))

        newGens = []
        for i in range(0, len(self._gens)):
            newGens.append(thisBotGenChances[i] and self._gens[i] or partner.getGens()[i])

        return Bot(newGens, self._solveFunction)

    def mutate(self, numberOfGens = 1):
        """
        Мутируем (изменяем случайным образом) случайный ген
        """
        for i in range(0, numberOfGens):
            targetGenIndex = random.randint(0, len(self._gens) - 1)
            currentValue = self._gens[targetGenIndex]
            if currentValue == 0:
                self._gens[targetGenIndex] = np.random.uniform(-100.0, 100.0)
            else:
                change = (random.random() * 4 - 2)
                self._gens[targetGenIndex] = self._gens[targetGenIndex] + self._gens[targetGenIndex] * change

    def getSolveFunction(self):
        return self._solveFunction

    def _isCompatible(self, bot):
        """
        Проверяем переданный bot - тип Bot и имеет туже solve функцию
        """
        if type(bot) is not Bot:
            return False
        if type(bot.getSolveFunction()) is not type(self._solveFunction):
            return False
        return True


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
        self._lastErrors = []

    def getGeneration(self):
        return self._generation

    def selectBestAndGenerate(self, trainMatrix, numberOfBest):
        """
        Выбираем лучшего представителя (с минимальной ошибкой - значением cost функции) и
        генерируем новое поколение из лучших
        """

        estimations = self._collectEstimations(trainMatrix, numberOfBest)
        bestBotEstimation = estimations[0]
        self._addLastError(bestBotEstimation.getError())

        bestBots = list(map(lambda estim: estim.getBot(), estimations))

        # Оставляем лучших представителей
        for i in range(0, numberOfBest):
            self.bots[i] = bestBots[i]

        weight = self._getMutationWeight()
        if weight > 1:
            log.info(f"Increase mutation weight: {weight}")

        # Создаем новое поколение из лучших представителей текущего
        for i in range(numberOfBest, len(self.bots)):
            parent1 = bestBots[random.randint(0, numberOfBest - 1)]
            parent2 = bestBots[random.randint(0, numberOfBest - 1)]
            child = parent1.reproduce(parent2)
            child.mutate(weight)
            self.bots[i] = child

        # Увеличиваем generation
        self._generation = self._generation + 1

        # Возвращаем ошибки лучшего бота текущей генерации
        return bestBotEstimation

    def _getMutationWeight(self):
        if len(self._lastErrors) <= 1:
            return 1
        lastError = self._lastErrors[-1]
        if not self._isErrorsDeviationSmall() or lastError < 0.1:
            return 1

        if lastError < 1:
            return 2
        if lastError < 10:
            return 3
        elif lastError < 100:
            return 4
        else:
            return 5

    def _addLastError(self, error):
        self._lastErrors.append(error)
        self._lastErrors = self._lastErrors[-5:]

    def _isErrorsDeviationSmall(self):
        return np.std(self._lastErrors) < 0.01

    def _collectEstimations(self, trainMatrix, numberOfBest):
        """
        Собираем лучших ботов с наименьшими ошибками
        """

        # seems not thread safe
        pool = Pool(cpu_count())
        dt = current_millis()
        estims = pool.map(partial(self._collectEstimation, trainMatrix = trainMatrix), self.bots)
        smallestEstims = heapq.nsmallest(numberOfBest, estims, key=lambda estim: estim.getError())
        pool.terminate()
        log.info(f" -> epoch computation duration {current_millis() - dt}ms")
        return sorted(smallestEstims, key=lambda estim: estim.getError())

        # estims = list(map(lambda bot: Estimation(bot, trainMatrix, self._costFunction), self.bots))
        # return sorted(estims, key=lambda estim: estim.getError())[:numberOfBest]

    def _collectEstimation(self, bot, trainMatrix):
        return Estimation(bot, trainMatrix, self._costFunction)

class Estimation:
    """
    Класс - контейнер, содержащий бота и его "ошибки", а так же среднюю ошибку
    """

    def __init__(self, bot, trainMatrix, costFunction):
        self._bot = bot
        self.__calculateBot(trainMatrix, costFunction)

    def __calculateBot(self, trainMatrix, costFunction):
        """
        Считаем выходные значение бота для каждого тренировочного значения из trainMaxtrix, где взодные значения берутся из нулевой колонки.
        Далее вычисляем ошибки всех входных значений путем сравнения с эталонными значениями в trainMatrix. 
        Эталонные значения ожидаются в первой колонке
        """
        self._values = self._bot.calculate(trainMatrix[:, 0])
        ethalons = trainMatrix[:, 1]

        self._errors = []
        for i in range(0, len(self._values)):
            self._errors.append(costFunction(self._values[i], ethalons[i]))

        self._meanError = np.mean(self._errors)

    def getValues(self):
        return self._values

    def getErrors(self):
        return self._errors

    def getBot(self):
        return self._bot

    def getError(self):
        return self._meanError


class PopulationContext:
    def costFunction(self, costFunction):
        self.costFunction = costFunction
        return self

    def botSolveFunction(self, botSolveFunction):
        self.botSolveFunction = botSolveFunction
        return self

    def botsNumberInPopulation(self, botsNumber):
        self.botsNumber = botsNumber
        return self

    def botsChromosomeSize(self, botsChromosomeSize):
        self.botsChromosomeSize = botsChromosomeSize
        return self

    def epochsNumber(self, epochsNumber):
        self.epochsNumber = epochsNumber
        return self

    def data(self, data):
        self.data = data
        return self

    def botsNumberToReproduce(self, botsNumberToReproduce):
        self.botsNumberToReproduce = botsNumberToReproduce
        return self


def generatePopulation(costFunction, botSolveFunction, numberOfBots, botChromosomeSize):
    bots = []
    for b in range(0, numberOfBots):
        bots.append(Bot.create(botSolveFunction, botChromosomeSize))

    return Population(costFunction, bots)


def runPopulation(context: PopulationContext, drawFun):
    # Create population
    population = generatePopulation(context.costFunction, context.botSolveFunction, \
                                    context.botsNumber, context.botsChromosomeSize)
    log.info("Prepared bots, population")  # , polynomPopulation)

    # Run the prepared population
    log.info("Launch world...")
    for e in range(0, context.epochsNumber):
        bestBotEstimation = population.selectBestAndGenerate(context.data, context.botsNumberToReproduce)
        log.info(f"Epoch: {e}, error: {bestBotEstimation.getError()}")

        if drawFun:
            drawFun(bestBotEstimation, e)

    return bestBotEstimation
