from pyspark.sql import SparkSession
from pyspark.sql.types import *

import matplotlib.pyplot as plt
import matplotlib.animation as anim
import matplotlib.gridspec as gridspec

from wordcloud import WordCloud

import re
import csv
import numpy as np
import os


class Dashboard:
    def __init__(self):
        self.DATASET_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "projData", "dataset")

        self.gs = gridspec.GridSpec(2, 2)
        self.fig = plt.figure(figsize=(10, 10))

        self.ax = plt.subplot(self.gs[0, 0])
        self.ax2 = plt.subplot(self.gs[0, 1])
        self.ax3 = plt.subplot(self.gs[1, :])

    def update(self, i):
        # add check on empty csv
        """chart update section"""
        self.pie_chart()

        self.get_hashtag()
        self.get_popular_hashtag()

        self.show_wordcloud()

        self.show_histogram()

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
        hashtag_as_string = ""
        for word in self.popular_hashtag[:100]:
            hashtag_as_string += word + " "

        wc = WordCloud(
            width=1000,
            height=1000,
            max_words=200,
            scale=3
        ).generate(hashtag_as_string)
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

        labels = pos_dict.keys()
        x = np.arange(len(labels))  # posizione dei livelli
        width = 0.35  # spessore delle barre

        with open(self.DATASET_FILE, "r") as raw_data:
            reader = csv.reader(raw_data, delimiter=",")
            for line in reader:
                for tag in neg_dict.keys():
                    if tag in line[0]:
                        if float(line[1]) > 0.0:  # positive
                            pos_dict[tag] += 1
                        if float(line[1]) < 1.0:  # negative
                            neg_dict[tag] += 1

        self.ax3.clear()

        fig, ax = plt.subplots()
        rects1 = self.ax3.bar(x - width / 2, pos_dict.values(), width, label='Positive', color='y')
        rects2 = self.ax3.bar(x + width / 2, neg_dict.values(), width, label='Negative', color='g')


        ax.set_xticks(x)

        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)

        fig.tight_layout()


        self.ax3.set_xticks(np.arange(len(neg_dict.keys())))
        self.ax3.set_xticklabels(neg_dict.keys(), rotation=90)
        # add legenda
        self.ax3.autoscale()

    def show_histogram_2(self):
        neg_dict = dict.fromkeys(self.popular_hashtag[:50], 0)
        pos_dict = dict.fromkeys(self.popular_hashtag[:50], 0)

        with open(self.DATASET_FILE, "r") as raw_data:
            reader = csv.reader(raw_data, delimiter=",")
            for line in reader:
                for tag in neg_dict.keys():
                    if tag in line[0]:
                        if float(line[1]) > 0.0:  # positive
                            pos_dict[tag] += 1
                        if float(line[1]) < 1.0:  # negative
                            neg_dict[tag] += 1

        labels = pos_dict.keys()

        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width / 2, pos_dict.values(), width, label='Positive', color='y')
        rects2 = ax.bar(x + width / 2, neg_dict.values(), width, label='Negative', color='g')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Sentiment')
        ax.set_title('Polarità nei giorni')
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=40)
        ax.legend()

        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)
        fig.tight_layout()
        ax.invert_xaxis()
        plt.show()


def run():
    foo = Dashboard()
    foo.animate()
    plt.show()


run()
