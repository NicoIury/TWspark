import matplotlib.pyplot as plt
import time

""""
def plot_data(data):
    plt.figure()
    ln, = plt.plot([])
    plt.ion()
    plt.show()
    while True:
        plt.pause(1)
        ln.set_xdata(range(len(data)))
        ln.set_ydata(data)
        plt.draw()
"""


def run(q):
    while 1:
        if q:
            test = q.get()
            print(test)
            # plot_data(test)



