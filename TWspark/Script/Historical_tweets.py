from pyspark.sql import *
import pyspark.sql.functions as f
from pyspark.ml import PipelineModel

import MLmodel
import os
from tkinter import *

import numpy as np
import matplotlib.pyplot as plt


class HistoricalApp:
    def __init__(self, root):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "projData", "data.json")
        self.spark = SparkSession.builder.appName("historical_tweets").getOrCreate()
        self.df = self.spark.read.option("multiLine", True).option("mode", "PERMISSIVE").json(path)
        udf_to_string = f.udf(lambda x: ",".join(x))
        self.df = self.df.withColumn("hashtag_list", udf_to_string(f.col("hashtag_list")))
        self.hashtagList = []

        self.clean()

        self.apply_model()
        self.df = self.df.select("hashtag_list", "time", "prediction")
        self.extract_hashtag()
        self.get_popular_hashtag()

        """ GUI section """
        root.geometry("300x400")
        self.Gen = root
        self.Gen.title("Historical_analysis")
        self.frame = Frame(self.Gen)
        self.frame.place(x=10, y=10)
        self.draw()

    def clean(self):
        regex = r"(http.\S+)|(@[^\s]+)"
        self.df = self.df.withColumn("text", f.lower(f.col("text")))
        self.df = self.df.withColumn("text", f.regexp_replace(f.col("text"), regex, ""))
        self.df = self.df.filter(self.df.text.isNotNull() & (self.df.text != ""))
        self.df.na.drop()

    def apply_model(self):
        sentiment_model = PipelineModel.load(os.path.join(MLmodel.MODEL_PATH, "pipe_model"))
        self.df = sentiment_model.transform(self.df)

    def extract_hashtag(self):
        for row in self.df.collect():
            if row.hashtag_list:
                for hash in row.hashtag_list.split(","):
                    self.hashtagList.append(hash)

    def get_popular_hashtag(self):
        all_hashtag = dict.fromkeys(self.hashtagList, 0)
        self.popular_hashtag = []
        for word in self.hashtagList:
            all_hashtag[word] += 1
        for item in (sorted(all_hashtag.items(), key=lambda x: x[1], reverse=True)):
            self.popular_hashtag.append(item[0])

    def draw(self):
        for i in range(10):
            label = Label(self.frame, text=self.popular_hashtag[i])
            label.grid(column=1, row=i+1)
            button = Button(self.frame, text="compute", command=lambda index=i: self.compute(index))
            button.grid(column=2, row=i+1)

    def compute(self, i):
        ht = self.popular_hashtag[i]
        time_list = []
        tmp_df = self.df.filter(self.df.hashtag_list.contains(ht))
        tmp_df = tmp_df.select(f.date_trunc("day", tmp_df.time).alias("time"), tmp_df.prediction)

        for row in tmp_df.collect():
            time_list.append(row.time.strftime("%d-%b-%Y"))

        neg_dict = dict.fromkeys(time_list, 0)
        pos_dict = dict.fromkeys(time_list, 0)

        for row in tmp_df.collect():
            if row.prediction > 0.0:  # positive case
                pos_dict[row.time.strftime("%d-%b-%Y")] += 1
            if row.prediction < 1.0:  # negative case
                neg_dict[row.time.strftime("%d-%b-%Y")] += 1

        print("selected hashtag: {}".format(ht))
        print(neg_dict, "\n\n", pos_dict)
        week_histogram(pos_dict, neg_dict, ht)  # creazione del grafico dopo aver selezionato l'hashtag


def week_histogram(pos_dict, neg_dict, hashtag):

    print("plotting values: \nPositive: {}\nNegative: {}".format(pos_dict.values(), neg_dict.values()))
    x = np.arange(len(pos_dict.keys()))

    labels = pos_dict.keys()
    fig, ax = plt.subplots()

    ax.plot(x, pos_dict.values(), label="Positive", color='y')
    ax.plot(x, neg_dict.values(), label="Negative", color='g')

    ax.set(xlabel='Day', ylabel='sentiment', title=hashtag)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=40)
    ax.grid()
    ax.legend()

    ax.invert_xaxis()
    plt.show()


def main():
    root = Tk()
    foo = HistoricalApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
