from pyspark.sql import *

from pyspark.ml import PipelineModel

import MLtest
import os
from tkinter import *


class HistoricalApp:
    def __init__(self, root):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "projData", "data.json")
        self.spark = SparkSession.builder.appName("historical_tweets").getOrCreate()
        self.df = self.spark.read.option("multiLine", True).option("mode", "PERMISSIVE").json(path)
        self.hashtagList = []

        # self.clean()

        self.apply_model()
        self.df = self.df.select("hashtag_list", "text", "time")
        self.extract_hashtag()
        self.get_popular_hashtag()

        """ GUI section """
        root.geometry("250x400")
        self.Gen = root
        self.Gen.title("Historical_analysis")
        self.frame = Frame(self.Gen)
        self.frame.place(x=10, y=10)
        self.draw()

    def clean(self):
        pass

    def apply_model(self):
        sentiment_model = PipelineModel.load(os.path.join(MLtest.MODEL_PATH, "pipe_model"))
        self.df = sentiment_model.transform(self.df)

    def extract_hashtag(self):
        tmp = []
        [tmp.append(row.hashtag_list) for row in self.df.collect()]
        for i in tmp:
            for j in i:
                if j:
                    self.hashtagList.append(j)

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
        pos_dict = {}
        neg_dict = {}
        # group df by day
        # search ht in df -> get count of neg/pos for every day (dict: (<day>, <count>))


def main():
    root = Tk()
    foo = HistoricalApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
