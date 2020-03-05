from pyspark.streaming import StreamingContext

from pyspark.sql.types import StructType, StructField, StringType
import pyspark.sql.functions as f
from pyspark.sql import SparkSession


from pyspark.ml import PipelineModel

import MLmodel

import os
import csv


def catch_stream():
    ssc = StreamingContext(spark.sparkContext, 10)
    host = "localhost"
    port = 5555

    lines = ssc.socketTextStream(host, port)

    lines.foreachRDD(to_df)

    ssc.start()
    ssc.awaitTermination()


def to_df(rdd):
    df = spark.createDataFrame(rdd.map(lambda x: (x, )), schema=SCHEMA)
    df = clean_df(df)
    apply_model(df)


def clean_df(df):
    df = df.withColumn("text", f.regexp_replace(f.col("text"), "(^RT)|(@[^\s]+)|(http.\S+)", ""))
    df = df.withColumn("text", f.trim(f.col("text")))
    df = df.filter(df.text.isNotNull() & (df.text != ""))
    df = df.withColumn("text", f.lower(f.col("text")))
    return df


def apply_model(df):
    pred = sentiment_model.transform(df)
    extract_data(pred)


def extract_data(pred_df):
    with open(DATASET_FILE, "a") as f:
        for row in pred_df.collect():
            wr = csv.writer(f)
            wr.writerow([row.text, row.prediction])


def refresh_file(path):
    if os.path.exists(path):
        os.remove(path)
        open(path, "a").close()


DATASET_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "projData", "dataset")
refresh_file(DATASET_FILE)

SCHEMA = StructType([StructField("text", StringType(), True)])
spark = SparkSession.builder.getOrCreate()
sentiment_model = PipelineModel.load(os.path.join(MLmodel.MODEL_PATH, "pipe_model"))

catch_stream()
