import numpy as np

def cost(ethalonY, botOutput):
    """Функция приспособленности - в данном случае cost функция - разница между эталонным значением
    и результатом расчета ботом с его Solve функцией."""
    return abs(ethalonY - botOutput)

def polymon(inputValue, gens):
    """Solve функция полиномиального вида: y = a0 + a1*x + a2*x^2 + a3*x^3 + ... + an*x^n
    где a0 - an - значения ген бота,
    x - входное значение
    y - выходное значение"""
    
    if len(gens) == 0:
        return 0.0
        
    value = gens[0]

    for ind in range(1, len(gens), 1): 
        value = value + gens[ind] * np.power(inputValue, ind)

    return value

def sinCos(inputValue, gens):
    """Solve  функция вида: a0 + a1*sin(x) + a2*sin(2*x) + a3*sin(3*x) + ... + an*sin(n*x) +
    + b1*cos(x) + b2*cos(2*x) + b3*cos(3*x) + ... bn*cos(n*x)
    где a0-an, b1-bn - значения ген бота,
    x - входное значение,
    y - выходное значение"""

    if len(gens) == 0:
        return 0.0
        
    halfIndex = len(gens) / 2
    
    value = gens[0]

    for a in range(1, halfIndex, 1):
        value = value + gens[a] * np.sin(input * a)

    for b in range(halfIndex,  len(gens), 1):
        value = value + gens[b] * np.cos(input * (b - halfIndex + 1))

    return value

def calcError(value, ethalon):
    """
    Вычисляет ошибку между переданным занчением и эталонным значением. Возвращает абсолютное значение (без учета значка ошибки)
    """
    return abs(ethalon - value)

def calcSquareError(value, ethalon):
    """
    Вычисляет квадратичную ошибку между переданным занчением и эталонным значением
    """
    return (ethalon - value)**2
