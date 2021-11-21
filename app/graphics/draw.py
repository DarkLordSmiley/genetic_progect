import matplotlib.pyplot as plt


class Draw:
    """
    Вспомогательный класс для изображения графиков.
    Draw - обертка для Figure
    """

    def __init__(self, title):
        """
        Конструктор для создания draw
        """
        self._fig, self._ax = plt.subplots()
        self._ax.set_title(title)
        plt.ion()
        plt.show()

    def draw(self, name, x, y):
        self._ax.plot(x, y, label=name)
        self._ax.legend()
        self._fig.canvas.draw()
        plt.pause(0.001)

    def finish(self):
        plt.ioff()
        plt.show()

