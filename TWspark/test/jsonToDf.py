from pyspark.sql import *
import os


def create_df(path):
    spark = SparkSession.builder.appName("historical_tweets").getOrCreate()
    df = spark.read.option("multiLine", True).option("mode", "PERMISSIVE").json(path)
    df.show()

if __name__ == "__main__":
    create_df(os.path.join(os.path.dirname(os.path.dirname(__file__)), "projData", "data.json"))
