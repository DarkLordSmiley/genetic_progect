import numpy as np
import random
import function

def getSquareError(errors):
    return np.square(errors).mean()

class Bot:
    """
    Бот - это организм, содержащий хромосому, т.е. набор генов для решения задачи.
    Каждый ген - это в полиноме - коэффициент при соответсвтующей степени, в других solve функциях - коэффициент при соответствующем
    члене ряда (последоваительности)
    Бот так же содержит ссылку на Solve функцию, которую применяет к своим хромосомам
    для нахождения Аллели - решения данного организма. Это решение может использоваться
    для оценки приспособленности данного организма
    """

    def __init__(self, gens, solveFunction):
        """
        Конструктор для создания бота на основе существующего набора ген
        """
        self._gens = gens
        self._solveFunction = solveFunction

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

    def calculate(self, inputs):
        """
        Вычисляем значение solve функции на основе значений генов этого
        экземпляра бота
        """
        return map(inputs, lambda val: self._solveFunction(val, self._gens))

    def getGens(self):
        return self._gens

    def reproduce(self, partner):
        """
        Генерируем потомка из ген этого бота и переданного. Выбираем гены случайным образом
        """
        if not self._isCompatible(partner):
            raise Exception("Parner bot is not compatible")
        
        thisBotGenChances = np.random.choice([True, False], size = len(self._gens))
        
        newGens = []
        for i in range(0, len(self._gens)):
            newGens.append(thisBotGenChances[i] and self._gens[i] or partner.getGens[i], thisBotGenChances)
            
        return Bot(newGens, self._solveFunction)

    def mutate(self):
        """
        Мутируем (изменяем случайным образом) случайный ген
        """
        targetGenIndex = random.randint(0, len(self._gens))
        change = random.random() * 2 - 1;
        self._gens[targetGenIndex] = self._gens[targetGenIndex] + self._gens[targetGenIndex] * change;

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

    def getGeneration(self):
        return self._generation
    
    def selectBestAndGenerate(self, trainMatrix, numberOfBest):
        """
        Выбираем лучшего представителя (с минимальной ошибкой - значением cost функции) и
        генерируем новое поколение из лучших
        """

        estimations = self._collectEstimations(trainMatrix, numberOfBest)
        bestBotEstimation = estimations[0]

        bestBots = map(lambda estim: estim.getBot(), estimations)

        # Создаем новое поколение из лучших представителей текущего
        for i in range(0, len(self.bots)) :
            parent1 = bestBots[random.randint(0, numberOfBest)]
            parent2 = bestBots[random.randint(0, numberOfBest)]
            child = parent1.reproduce(parent2)
            child.mutate()
            self.bots[i] = child

        # Увеличиваем generation
        self._generation = self._generation + 1

        # Возвращаем ошибки лучшего бота текущей генерации
        return bestBotEstimation.getErrors()
    
    def _collectEstimations(self, trainMatrix, numberOfBest):
        """
        Собираем лучших ботов с наименьшими ошибками
        """
        inputs = trainMatrix[:, 0]
        estims = map(lambda bot: Estimation(bot, inputs), self.bots)
        return sorted(estims, key = lambda estim: estim.getError)[:numberOfBest]

class Estimation:
    """
    Класс - контейнер, содержащий бота и его "ошибки", а так же среднюю ошибку
    """

    def __init__(self, bot, trainMatrix):
        self._bot = bot
        self.__calculateBot(trainMatrix)
    
    def __calculateBot(self, trainMatrix):
        """
        Считаем выходные значение бота для каждого тренировочного значения из trainMaxtrix, где взодные значения берутся из нулевой колонки.
        Далее вычисляем ошибки всех входных значений путем сравнения с эталонными значениями в trainMatrix. 
        Эталонные значения ожидаются в первой колонке
        """
        self._values = self._bot.calculate(trainMatrix[:, 0])
        ethalons = trainMatrix[:,1]

        self._errors = []
        for i in range(0, len(self._values)):
            self._errors.append(function.calcError(self._values[i], ethalons[i]))

        self._meanError = np.mean(self._errors)

    def getValues(self):
        return self._values

    def getErrors(self):
        return self._errors

    def getBot(self):
        return self._bot
    
    def getError(self):
        return self._meanError
    