import matplotlib.pyplot as plt
import matplotlib.animation as anim


class dashboard:
    def __init__(self):
        self.PRED_FILE = "/home/nico/Nico/pyProg/projData/PredList"
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)

    def update(self, i):
        # self.y = []
        neg_op = []
        pos_op = []
        raw_data = open(self.PRED_FILE, "r").read().split("\n")
        for line in raw_data:
            try:
                tmp = (float(line.replace("\n", "")))
                if tmp > 0.0: # positive
                    pos_op.append(tmp)
                if tmp < 1.0: # negative
                    neg_op.append(tmp)
            except ValueError:
                pass
        value = [(len(pos_op)), (len(neg_op))]
        self.ax.clear()
        self.ax.pie(value, labels=["positive", "negative"], colors=["yellow", "green"], autopct='%1.1f%%',
                    explode=(0, 0.1), shadow=True, startangle=140)

        """hashtag wordcloud"""


        """linear plot"""
        """
        self.x = list(range(len(self.y)))

        print(self.x, self.y)
        self.ax.plot(self.x, self.y) #esce de capa
        """

    def animate(self):
        self.a = anim.FuncAnimation(self.fig, self.update, interval=100, repeat=False)


def run():
    foo = dashboard()
    foo.animate()
    plt.show()


run()
