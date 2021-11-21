import numpy as np
import app.algorithm.model as model
from app.graphics import draw as draw

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
        error = round(estimation.getErrors()[0], 5)
        draw.draw(f"E:{epoch}, err.:{error}", x, y)
