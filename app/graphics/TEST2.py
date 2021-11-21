import matplotlib.pyplot as plt
import time
import draw

dr = draw.Draw("Test")
dr.draw('Test1', [-10, -5, -2, -1, 0, 1, 2, 5, 10], [-20, -10, -4, -2, 0, 2, 4, 10, 20])
time.sleep(1)
# plt.pause(1)
dr.draw('Test2', [-10, -5, -2, -1, 0, 1, 2, 5, 10], [-10, -5, -2, -1, 0, 1, 2, 5, 10])
time.sleep(1)
# plt.pause(1)
dr.draw('Test3', [-10, -5, -2, -1, 0, 1, 2, 5, 10], [-5, -2.5, -1, -0.5, 0, 0.5, 1, 2.5, 5])

dr.finish()
