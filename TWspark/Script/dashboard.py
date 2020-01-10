import matplotlib.pyplot as plt
import matplotlib.animation as anim


class dashboard:
    def __init__(self):
        self.PRED_FILE = "/home/nico/Nico/pyProg/projData/PredList"
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)

    def update(self, i):
        self.y = []

        raw_data = open(self.PRED_FILE, "r").read().split("\n")
        for line in raw_data:
            try:
                self.y.append(float(line.replace("\n", "")))
            except ValueError:
                pass

        self.x = list(range(len(self.y)))

        print(self.x, self.y)
        self.ax.plot(self.x, self.y) #esce de capa

    def animate(self):
        self.a = anim.FuncAnimation(self.fig, self.update, interval=1000)


def run():
    foo = dashboard()
    foo.animate()
    plt.show()


run()
