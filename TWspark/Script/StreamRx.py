from pyspark.streaming import StreamingContext

from pyspark.sql.types import StructType, StructField, StringType
import pyspark.sql.functions as f
from pyspark.sql import SparkSession


from pyspark.ml import PipelineModel

import MLtest

import os
import csv
import string


def catch_stream():
    ssc = StreamingContext(spark.sparkContext, 10)
    host = "localhost"
    port = 5555
    lines = ssc.socketTextStream(host, port)

    lines.foreachRDD(to_df)
    # test(lines)

    ssc.start()
    ssc.awaitTermination()


def test(lines):
    """wcount in tweets"""
    words = lines.flatMap(lambda line: line.split(" "))
    pairs = words.map(lambda word: (word, 1))
    count = pairs.reduceByKey(lambda x, y: x+y)
    count.pprint()


def to_df(rdd):
    df = spark.createDataFrame(rdd.map(lambda x: (x, )), schema=SCHEMA)
    # df.show()
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
    pred.show()
    extract_data(pred)


def extract_data(pred_df):
    """
    [QUEUE.put(float(pred.prediction)) for pred in pred_df.collect()]

    with open(PRED_FILE, "a") as f:
        [f.write(str(pred.prediction)+"\n") for pred in pred_df.collect()]

    with open(TEXT_FILE, "a") as g:
        [g.write(str(text.text)) for text in pred_df.collect()]
    """
    with open(DATASET_FILE, "a") as f:
        for row in pred_df.collect():
            wr = csv.writer(f)
            wr.writerow([row.text, row.prediction])


def refresh_file(path):
    if os.path.exists(path):
        os.remove(path)
        open(path, "a").close()

"""
TEXT_FILE = "/home/nico/Nico/pyProg/projData/TextList"
PRED_FILE = "/home/nico/Nico/pyProg/projData/PredList"
refresh_file(TEXT_FILE)
refresh_file(PRED_FILE)
"""
DATASET_FILE = "/home/nico/Nico/pyProg/projData/dataset"
refresh_file(DATASET_FILE)

SCHEMA = StructType([StructField("text", StringType(), True)])
spark = SparkSession.builder.getOrCreate()
sentiment_model = PipelineModel.load(os.path.join(MLtest.MODEL_PATH, "pipe_model"))

catch_stream()

"""
QUEUE = multiprocessing.Queue()

pr1 = multiprocessing.Process(target=catch_stream)
pr1.start()
pr2 = multiprocessing.Process(target=dashboard.run(QUEUE))
pr2.start()

pr1.join()
pr2.join()
"""