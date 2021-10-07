import numpy as np

class Bot:
    """Бот - это организм, содержащий хромосому, т.е. набор генов для решения задачи.
    Бот так же содержит ссылку на Solve функцию, которую применяет к своим хромосомам
    для нахождения Аллели - решения данного организма. Это решение может использоваться
    для оценки приспособленности данного организма"""

    def __init__(self, solveFunction, chromosomeSize: int):
        """Конструктор с Solve функцией и размером хромосомы - т.е. кол-вом ген."""
        self._solveFunction = solveFunction
        self._gens = self._initGens(chromosomeSize)

    def _initGens(self, chromosomeSize: int):
        """Создает массив ген указанного в chromosomeSize размера и инициализирует его
        случайными значениями float"""

        return np.random.uniform(-100.0, 100.0, chromosomeSize)
        
