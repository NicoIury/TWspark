import matplotlib.pyplot as plt
import matplotlib.animation as anim
import matplotlib.gridspec as gridspec

from wordcloud import WordCloud

import re
import csv
import numpy as np
import os
from collections import Counter


class Dashboard:
    def __init__(self):
        self.DATASET_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "projData", "dataset")

        self.gs = gridspec.GridSpec(2, 2)
        self.fig = plt.figure(figsize=(10, 10))

        self.ax = plt.subplot(self.gs[0, 0])
        self.ax2 = plt.subplot(self.gs[0, 1])
        self.ax3 = plt.subplot(self.gs[1, :])

    def update(self, i):
        """chart update section"""
        try:
            self.pie_chart()

            self.get_hashtag()
            self.get_popular_hashtag()

            self.show_wordcloud()

            self.show_histogram()

        except Exception as e:
            print(e)

    def animate(self):
        self.a = anim.FuncAnimation(self.fig, self.update, interval=100, repeat=False)

    def get_hashtag(self):
        self.hashtag = []
        with open(self.DATASET_FILE, "r") as raw_data:
            reader = csv.reader(raw_data, delimiter=",")
            for line in reader:
                for word in re.findall("#\w+", line[0]):
                    # add if not in self.hashtag.split()
                    self.hashtag.append(word)

    def get_popular_hashtag(self):
        all_hashtag = dict.fromkeys(self.hashtag, 0)
        self.popular_hashtag = []
        for word in self.hashtag:
            all_hashtag[word] += 1
        for item in (sorted(all_hashtag.items(), key=lambda x: x[1], reverse=True)):
            self.popular_hashtag.append(item[0])

    def show_wordcloud(self):
        hashtag_plus_freq = {}
        val = 100
        for word in self.popular_hashtag[:100]:
            hashtag_plus_freq[word] = val
            val = val - 1

        wc = WordCloud(
            width=1000,
            height=1000,
            max_words=200,
            scale=3
        ).generate_from_frequencies(hashtag_plus_freq)
        self.ax2.imshow(wc)

    def pie_chart(self):
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

    def show_histogram(self):
        neg_dict = dict.fromkeys(self.popular_hashtag[:50], 0)
        pos_dict = dict.fromkeys(self.popular_hashtag[:50], 0)

        x = np.arange(len(neg_dict.keys()))
        width = 0.35

        with open(self.DATASET_FILE, "r") as raw_data:
            reader = csv.reader(raw_data, delimiter=",")
            for line in reader:
                for tag in neg_dict.keys():
                    if tag in line[0]:
                        if float(line[1]) > 0.0:  # positive
                            pos_dict[tag] += 1
                        if float(line[1]) < 1.0:  # negative
                            neg_dict[tag] += 1

        new_neg_dict = {}
        new_pos_dict = {}

        dict_sum = dict(Counter(pos_dict) + Counter(neg_dict))

        for k in sorted(dict_sum, key=dict_sum.get, reverse=True):
            new_neg_dict[k] = neg_dict[k]
            new_pos_dict[k] = pos_dict[k]

        self.ax3.clear()

        self.ax3.bar(x - width / 2, new_pos_dict.values(), width, label='Positive', color='y')
        self.ax3.bar(x + width / 2, new_neg_dict.values(), width, label='Negative', color='g')

        self.ax3.set_xticks(np.arange(len(neg_dict.keys())))
        self.ax3.set_xticklabels(neg_dict.keys(), rotation=90)

        self.ax3.set_ylabel('Polarity value')
        self.ax3.set_title('Hashtag Polarity')

        self.ax3.autoscale()


def run():
    foo = Dashboard()
    foo.animate()
    plt.show()


if __name__ == "__main__":
    run()
