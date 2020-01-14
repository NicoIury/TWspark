import matplotlib.pyplot as plt
import matplotlib.animation as anim
import matplotlib.gridspec as gridspec

from wordcloud import WordCloud

import re 
import csv


class dashboard:
    def __init__(self):
        self.DATASET_FILE = "/home/nico/Nico/pyProg/projData/dataset"
        self.TEXT_FILE = "/home/nico/Nico/pyProg/projData/TextList"
        self.gs = gridspec.GridSpec(2, 2)
        self.fig = plt.figure(figsize=(10, 10))
        self.ax = plt.subplot(self.gs[0, 0])

    def update(self, i):
        # self.y = []
        neg_op = []
        pos_op = []
        with open(self.DATASET_FILE, "r") as raw_data:
            reader = csv.reader(raw_data, delimiter=",")
            for line in reader:
                try:
                    tmp = float(line[1])
                    if tmp > 0.0:  # positive
                        pos_op.append(tmp)
                    if tmp < 1.0:  # negative
                        neg_op.append(tmp)
                except ValueError:
                    pass

        value = [(len(pos_op)), (len(neg_op))]
        self.ax.clear()
        self.ax.pie(value, labels=["positive", "negative"], colors=["yellow", "green"], autopct='%1.1f%%',
                    explode=(0, 0.1), shadow=True, startangle=140, radius=1)

        """hashtag wordcloud"""
        self.show_wordcloud()
        """linear plot"""
        """
        self.x = list(range(len(self.y)))

        print(self.x, self.y)
        self.ax.plot(self.x, self.y) #esce de capa
        """

    def animate(self):
        self.a = anim.FuncAnimation(self.fig, self.update, interval=100, repeat=False)

    def get_hashtag(self):
        self.hashtag = ""
        with open(self.TEXT_FILE, "r") as raw_data:
            reader = csv.reader(raw_data, delimiter=",")
            for line in reader:
                for word in re.findall("#\w+", line[0]):
                    self.hashtag += " " + word

        # print(self.hashtag)

    def show_wordcloud(self):
        self.get_hashtag()
        self.ax2 = plt.subplot(self.gs[0, 1])
        wc = WordCloud(
            width=1000,
            height=1000,
            max_words=200,
            scale=3
        ).generate(self.hashtag)
        self.ax2.imshow(wc)


def run():
    foo = dashboard()
    foo.animate()
    plt.show()


run()
