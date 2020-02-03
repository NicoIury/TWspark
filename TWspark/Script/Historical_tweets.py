from pyspark.sql import *
import pyspark.sql.functions as f
from pyspark.ml import PipelineModel

import MLtest
import os
from tkinter import *
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


class HistoricalApp:
    def __init__(self, root):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "projData", "data.json")
        self.spark = SparkSession.builder.appName("historical_tweets").getOrCreate()
        self.df = self.spark.read.option("multiLine", True).option("mode", "PERMISSIVE").json(path)
        udf_to_string = f.udf(lambda x: ",".join(x))
        self.df = self.df.withColumn("hashtag_list", udf_to_string(f.col("hashtag_list")))
        self.hashtagList = []

        # self.clean()

        self.apply_model()
        self.df = self.df.select("hashtag_list", "time", "prediction")
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
                #print(pos_dict)
            if row.prediction < 1.0:  # negative case
                neg_dict[row.time.strftime("%d-%b-%Y")] += 1
                #print(neg_dict)
        # plotting neg_dict e pos_dict here
        print(f"selected hashtag: {ht}")
        self.week_histogram(pos_dict,neg_dict,ht) #creazione del grafico dopo aver selezionato l'hashtag

    def week_histogram(self,pos_dict,neg_dict,hashtag):
        print(f"Valori da plottare:\nPositivi: {pos_dict.values()}\nNegativi: {neg_dict.values()}")
        labels = pos_dict.keys()
        # men_means=pos_dict.values()
        # women_means=neg_dict.values()

        x = np.arange(len(labels))  # posizione dei livelli
        width = 0.35  # spessore delle barre

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width / 2, pos_dict.values(), width, label='Positive', color='y')
        rects2 = ax.bar(x + width / 2, neg_dict.values(), width, label='Negative', color='g')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Sentiment')  #titolo asse Y
        ax.set_title(hashtag)   #come titolo, l'hashtag selezionato
        ax.set_xticks(x)
        ax.set_xticklabels(labels,rotation=40 )
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
        ax.invert_xaxis() #ordine cronologico

        plt.show()


def main():
    root = Tk()
    foo = HistoricalApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
