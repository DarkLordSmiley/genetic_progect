import numpy
import numpy as np
import logging
import algorithm.model as model
from graphics import draw as draw


def cost(ethalonY, botOutput):
    """Функция приспособленности - в данном случае cost функция - разница между эталонным значением
    и результатом расчета ботом с его Solve функцией."""
    return abs(botOutput - ethalonY)

# ToDo: rework as classes
def polynom(inputValues, gens):
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
    inputs = np.array(inputValues)
    inMatrix = inputs[np.newaxis, :].T
    a_powers = inMatrix ** np.arange(len(gens))
    # Вектор степеней поэелементно умножаем на значение каждого гена и суммируем все значения
    # gens - это вектор [a0, a1, a2, a3, ...] умножаем его по вектор степеней, получаем вектор:
    # [a0*x^0, a1*x^1, a2*x^2, a3*x^3, ...]
    # и суммируем: value = a0*x^0 + a1*x^1 + a2*x^2 + a3*x^3, ...
    return np.sum(a_powers * gens, axis=1)

    # powers = np.power(inputValue, np.arange(len(gens)), dtype=np.float)
    # value = numpy.sum(np.multiply(powers, gens))
    # return value

def polynomToString(gens):
    """Функция для вывода в виде строки полинома с данными коэффициентами в виде:
    y = a0 + a1*x + a2*x^2 + a3*x^3 + ... + an*x^n
    где a0 - an - значения ген бота
    """
    if len(gens) == 0:
        return 'y=0'
    result = 'y='
    for (index, gen) in enumerate(gens):
        if index == 0:
            result = result + "{:0.4f}".format(gen)
        else:
            sign = (' +' if gen >= 0 else ' ')
            power = ('^' + str(index) if index > 1 else '')
            result = result + sign + "{:0.4f}".format(gen) + "*x" + power
    return result

def polynomSum(inputValues, gens):
    """Solve функция полиномиального вида: y = a0 + a1*x + a2*x^2 + a3*x^3 + ... + an*x^n
        + b0*x^(-1) + b1 * x^(-2) + b2 * x^(-3) + b3 * x^(-4) + ... + b(n-1) * a^(-n))
    где a0 - an, b0 - b(n-1) - значения ген бота
    Если кол-во ген четно, то используются len(gens)-1 ген
    x - входное значение
    y - выходное значение
    Вычисляет выходные значения для всех переданных входных значений.
    Используется vectorization для ускорения вычислений"""

    if len(gens) == 0:
        return 0.0

    if len(gens) % 2 == 0:
        length_a = int(len(gens) / 2)
    else:
        length_a = int((len(gens) + 1) / 2)

    length_b = length_a - 1

    a_array = gens[:length_a]
    b_array = gens[length_a:length_a + length_b]

    inputs = np.array(inputValues)
    inMatrix = inputs[np.newaxis, :].T
    a_powers = inMatrix ** np.arange(length_a)
    b_powers = inMatrix ** np.arange(-length_b, 0)[::-1]
    return np.sum(a_powers * a_array, axis=1) + np.sum(b_powers * b_array, axis=1)

    # Оптимизированный алгоритм (через векторы и numpy)
    # Возводим входное значение (inputValue) поочередно в степени b_array
    # результат - вектор степеней ([x^b0, x^b1, x^b2, x^b3, ...] где x - это inputValue
    #a_powers = np.power(inputValues, np.arange(length_a), dtype=np.float)
    #b_powers = np.power(inputValues, np.arange(-length_b, 0)[::-1], dtype=np.float)
    # Вектор степеней поэелементно умножаем на значение каждого гена и суммируем все значения
    # gens - это вектор [a0, a1, a2, a3, ...] умножаем его по вектор степеней, получаем вектор:
    # [a0*x^0, a1*x^1, a2*x^2, a3*x^3, ...]
    # и суммируем: value = a0*x^0 + a1*x^1 + a2*x^2 + a3*x^3, ...
    # value = np.sum(np.multiply(a_powers, a_array)) + np.sum(np.multiply(b_powers, b_array))
    # return value

def polynomSumToString(gens):
    """Функция для вывода в виде строки полинома с данными коэффициентами в виде:
    y = a0 + a1*x + a2*x^2 + a3*x^3 + ... + an*x^n
        + b0*x^(-1) + b1 * x^(-2) + b2 * x^(-3) + b3 * x^(-4) + ... + b(n-1) * a^(-n))
    где a0 - an, b0 - b(n-1) - значения ген бота
    Если кол-во ген четно, то используются len(gens)-1 ген
    """
    if len(gens) == 0:
        return 'y=0'

    if len(gens) % 2 == 0:
        length_a = int(len(gens) / 2)
    else:
        length_a = int((len(gens) + 1) / 2)

    length_b = length_a - 1

    a_array = gens[:length_a]
    b_array = gens[length_a:length_a + length_b]

    result = 'y='
    for (index, gen) in enumerate(a_array):
        if index == 0:
            result = result + "{:0.4f}".format(gen)
        else:
            sign = (' +' if gen >= 0 else ' ')
            power = ('^' + str(index) if index > 1 else '')
            result = result + sign + "{:0.4f}".format(gen) + "*x" + power
    for (index, gen) in enumerate(b_array):
            sign = (' +' if gen >= 0 else ' ')
            power = '^(-' + str(index + 1) + ')'
            result = result + sign + "{:0.4f}".format(gen) + "*x" + power

    return result

def polynomL(inputValues, gens):
    """Solve функция полиномиального вида:
    y = a0 + a1*(x + b1) + a2*(x + b2)^2 + a3*(x+b3)^3 + ... + an*(x+bn)^n
           + c1*(x + d1)^(-1) + c2*(x + d2)^(-2) + c3*(x+d3)^(-3) + ... + cn*(x+dn)^(-n)

    где a0 - an, b1 - bn, c1 - cn, d1 - dn - значения ген бота
    Соответственно минимальное кол-во ген = 5
    распределение в хромосоме: [a0, a1, ..., an, b1, ..., bn, c1, ..., cn, d1, ..., dn]
    соотвественно len(gens)-1 % 4 должно = 0
    Если кол-во ген четно, то используются len(gens)-1 ген
    x - входные значения
    y - выходные значения
    Вычисляет выходные значения для всех переданных входных значений.
    Используется vectorization для ускорения вычислений"""

    if len(gens) == 0:
        return 0.0

    if (len(gens) - 1) % 4 != 0:
        raise Exception("Gens number is not polynomL compliant. The (number-1) must be devided by 4")

    length = int((len(gens) - 1) / 4)
    a0 = gens[0]
    a_array = gens[1:length + 1]
    b_array = gens[length + 1 : length * 2 + 1]
    c_array = gens[length * 2 + 1 : length * 3 + 1]
    d_array = gens[length * 3 + 1 : length * 4 + 1]

    inputs = np.array(inputValues)
    inMatrix = inputs[np.newaxis, :].T
    x_b_sums = inMatrix + b_array
    x_d_sums = inMatrix + d_array
    a_powers = x_b_sums ** np.arange(1, length + 1)
    c_powers = x_d_sums ** np.arange(-length, 0)[::-1]

    return a0 + np.sum(a_powers * a_array, axis=1) + np.sum(c_powers * c_array, axis=1)

    # Оптимизированный алгоритм (через векторы и numpy)
    # Возводим входное значение (inputValue) поочередно в степени b_array
    # результат - вектор степеней ([x^b0, x^b1, x^b2, x^b3, ...] где x - это inputValue
    #a_powers = np.power(inputValues, np.arange(length_a), dtype=np.float)
    #b_powers = np.power(inputValues, np.arange(-length_b, 0)[::-1], dtype=np.float)
    # Вектор степеней поэелементно умножаем на значение каждого гена и суммируем все значения
    # gens - это вектор [a0, a1, a2, a3, ...] умножаем его по вектор степеней, получаем вектор:
    # [a0*x^0, a1*x^1, a2*x^2, a3*x^3, ...]
    # и суммируем: value = a0*x^0 + a1*x^1 + a2*x^2 + a3*x^3, ...
    # value = np.sum(np.multiply(a_powers, a_array)) + np.sum(np.multiply(b_powers, b_array))
    # return value

def polynomLToString(gens):
    """Функция для вывода в виде строки полинома с данными коэффициентами в виде:
    y = a0 + a1*(x + b1) + a2*(x + b2)^2 + a3*(x+b3)^3 + ... + an*(x+bn)^n
           + c1*(x + d1)^(-1) + c2*(x + d2)^(-2) + c3*(x+d3)^(-3) + ... + cn*(x+dn)^(-n)

    где a0 - an, b1 - bn, c1 - cn, d1 - dn - значения ген бота
    """
    if len(gens) == 0:
        return 'y=0'

    length = int((len(gens) - 1) / 4)
    a0 = gens[0]
    a_array = gens[1:length + 1]
    b_array = gens[length + 1 : length * 2 + 1]
    c_array = gens[length * 2 + 1 : length * 3 + 1]
    d_array = gens[length * 3 + 1 : length * 4 + 1]

    result = 'y=' + "{:0.4f}".format(a0)
    for i in range(0, length):
        a = a_array[i]
        b = b_array[i]
        sign = (' +' if a >= 0 else ' ')
        x_sign = (' +' if b >= 0 else ' ')
        power = ('^' + str(i + 1) if i > 0 else '')
        result = result + sign + "{:0.4f}".format(a) + "*(x" + x_sign + "{:0.4f}".format(b) +")" + power
    for i in range(0, length):
        c = c_array[i]
        d = d_array[i]
        sign = (' +' if c >= 0 else ' ')
        x_sign = (' +' if d >= 0 else ' ')
        power = '^(-' + str(i + 1) + ')'
        result = result + sign + "{:0.4f}".format(c) + "*(x" + x_sign + "{:0.4f}".format(d) +")" + power

    return result

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
