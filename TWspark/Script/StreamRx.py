from pyspark.streaming import StreamingContext

from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql import SparkSession


from pyspark.ml import PipelineModel

import MLtest
import dashboard

from os import path
import multiprocessing
import time


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
    apply_model(df)


def apply_model(df):
    pred = sentiment_model.transform(df)
    # pred.show()
    extract_prediction(pred)


def extract_prediction(pred_df):
    [QUEUE.put(float(pred.prediction)) for pred in pred_df.collect()]
    time.sleep(1)


SCHEMA = StructType([StructField("text", StringType(), True)])
spark = SparkSession.builder.getOrCreate()

sentiment_model = PipelineModel.load(path.join(MLtest.MODEL_PATH, "pipe_model"))

QUEUE = multiprocessing.Queue()

pr1 = multiprocessing.Process(target=catch_stream)
pr1.start()
pr2 = multiprocessing.Process(target=dashboard.run(QUEUE))
pr2.start()

pr1.join()
pr2.join()
