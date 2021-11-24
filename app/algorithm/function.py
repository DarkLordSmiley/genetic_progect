import numpy
import numpy as np
import algorithm.model as model
from graphics import draw as draw


def cost(ethalonY, botOutput):
    """Функция приспособленности - в данном случае cost функция - разница между эталонным значением
    и результатом расчета ботом с его Solve функцией."""
    return abs(botOutput - ethalonY)


def polymon(inputValue, gens):
    """Solve функция полиномиального вида: y = a0 + a1*x + a2*x^2 + a3*x^3 + ... + an*x^n
    где a0 - an - значения ген бота,
    x - входное значение
    y - выходное значение"""

    if len(gens) == 0:
        return 0.0

    # value = gens[0]
    # for ind in range(1, len(gens), 1):
    #     value = value + gens[ind] * np.power(inputValue, ind)

    # Оптимизированный алгоритм (через векторы и numpy)
    # Возводим входное значение (inputValue) поочередно в степени 0, 1, 2, 3 ... len(gens)
    # результат - вектор степеней ([x^0, x^1, x^2, x^3, ...] где x - это inputValue
    powers = np.power(inputValue, np.arange(len(gens)), dtype=np.float)
    # Вектор степеней поэелементно умножаем на значение каждого гена и суммируем все значения
    # gens - это вектор [a0, a1, a2, a3, ...] умножаем его по вектор степеней, получаем вектор:
    # [a0*x^0, a1*x^1, a2*x^2, a3*x^3, ...]
    # и суммируем: value = a0*x^0 + a1*x^1 + a2*x^2 + a3*x^3, ...
    value = numpy.sum(np.multiply(powers, gens))
    return value


def polymonSym(inputValue, gens):
    """Solve функция полиномиального вида: y = a0 + a1*x + a2*x^2 + a3*x^3 + ... + an*x^n
        + b0*x^(-1) + b1 * x^(-2) + b2 * x^(-3) + b3 * x^(-4) + ... + b(n-1) * a^(-n))
    где a0 - an, b0 - b(n-1) - значения ген бота
    Если кол-во ген нечетно, то используются len(gens)-1 ген
    x - входное значение
    y - выходное значение"""

    if len(gens) == 0:
        return 0.0

    if len(gens) % 2 != 0:
        length = int((len(gens) - 1) / 2)
    else:
        length = int(len(gens) / 2)

    a_array = gens[:length]
    b_array = gens[length:(length * 2)]

    # value = gens[0]
    # for ind in range(1, len(gens), 1):
    #     value = value + gens[ind] * np.power(inputValue, ind)

    # Оптимизированный алгоритм (через векторы и numpy)
    # Возводим входное значение (inputValue) поочередно в степени b_array
    # результат - вектор степеней ([x^b0, x^b1, x^b2, x^b3, ...] где x - это inputValue
    a_powers = np.power(inputValue, np.arange(length), dtype=np.float)
    b_powers = np.power(inputValue, np.arange(-length, 0)[::-1], dtype=np.float)
    # Вектор степеней поэелементно умножаем на значение каждого гена и суммируем все значения
    # gens - это вектор [a0, a1, a2, a3, ...] умножаем его по вектор степеней, получаем вектор:
    # [a0*x^0, a1*x^1, a2*x^2, a3*x^3, ...]
    # и суммируем: value = a0*x^0 + a1*x^1 + a2*x^2 + a3*x^3, ...
    value = np.sum(np.multiply(a_powers, a_array)) + np.sum(np.multiply(b_powers, b_array))
    return value

def power(inputValue, gens):
    """Solve функция вида: y = a0 + a1*x^b0 + a2*x^b1 + a3*x^b2 + ... + an*x^b(n-1)
    где a0 - an, b0 - b(n-1) - значения ген бота,
    x - входное значение (должны быть положительными, иначе возведение в действительную степень
    математически не всегда возможно)
    y - выходное значение"""

    if len(gens) == 0:
        return 0.0

    a0 = gens[0]

    length = int((len(gens) - 1) / 2)
    a_array = gens[1:length + 1]
    b_array = gens[length + 1 : length * 2 + 1]

    # value = gens[0]
    # for ind in range(1, len(gens), 1):
    #     value = value + gens[ind] * np.power(inputValue, ind)

    # Оптимизированный алгоритм (через векторы и numpy)
    # Возводим входное значение (inputValue) поочередно в степени b_array
    # результат - вектор степеней ([x^b0, x^b1, x^b2, x^b3, ...] где x - это inputValue
    powers = np.power(inputValue, b_array, dtype=np.float)
    # В случае отрицательного входного значения np.power выдает nan - меняем на 0
    powers[np.isnan(powers)] = 0
    # Вектор степеней поэелементно умножаем на значение каждого гена и суммируем все значения
    # gens - это вектор [a0, a1, a2, a3, ...] умножаем его по вектор степеней, получаем вектор:
    # [a0*x^0, a1*x^1, a2*x^2, a3*x^3, ...]
    # и суммируем: value = a0*x^0 + a1*x^1 + a2*x^2 + a3*x^3, ...
    value = a0 + numpy.sum(np.multiply(powers, a_array))
    return value

def sinCos(inputValue, gens):
    """Solve  функция вида: a0 + a1*sin(x) + a2*sin(2*x) + a3*sin(3*x) + ... + an*sin(n*x) +
    + b1*cos(x) + b2*cos(2*x) + b3*cos(3*x) + ... bn*cos(n*x)
    где a0-an, b1-bn - значения ген бота,
    x - входное значение,
    y - выходное значение"""

    if len(gens) == 0:
        return 0.0

    a0 = gens[0]
    a_array = gens[1:]

    halfIndex = int(len(a_array) / 2)

    value = a0

    for a in range(0, halfIndex):
        k = a + 1
        value = value + a_array[a] * np.sin(inputValue * k)

    for b in range(halfIndex, len(a_array), 1):
        k = b - halfIndex + 1
        value = value + a_array[b] * np.cos(inputValue * k)

    return value


def drawEstimation(draw: draw.Draw, estimation: model.Estimation, epoch, context: model.PopulationContext):
    if epoch < 5 or epoch % 10 == 0:
        x = context.data[:, 0]
        y = estimation.getValues()
        error = round(estimation.getError(), 5)
        draw.draw(f"E:{epoch}, err.:{error}", x, y)
