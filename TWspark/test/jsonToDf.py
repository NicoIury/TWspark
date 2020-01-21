from pyspark.sql import *


def create_df(path):
    spark = SparkSession.builder.appName("historical_tweets").getOrCreate()
    df = spark.read.option("multiLine", True).option("mode", "PERMISSIVE").json(path)
    df.show()

if __name__ == "__main__":
    create_df("/home/nico/Nico/pyProg/projData/data.json")
