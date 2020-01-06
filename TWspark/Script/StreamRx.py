from pyspark.streaming import StreamingContext

from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql import SparkSession

SCHEMA = StructType([StructField("text", StringType(), True)])

spark = SparkSession.builder.getOrCreate()


def catch_stream():

    ssc = StreamingContext(spark.sparkContext, 10)
    host = "localhost"
    port = 5555
    lines = ssc.socketTextStream(host, port)

    lines.foreachRDD(to_df)
    #test(lines)

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
    df.show()
    #apply_model(df)


def apply_model(df):
    pass


if __name__ == "__main__":
    catch_stream()
