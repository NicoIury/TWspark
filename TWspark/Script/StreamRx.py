from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import *


def get_stream():
    sc = SparkContext()
    ssc = StreamingContext(sc, 10)
    host = "localhost"
    port = 5555
    lines = ssc.socketTextStream(host, port)

    words = lines.flatMap(lambda line: line.split(" "))
    pairs = words.map(lambda word: (word, 1))
    count = pairs.reduceByKey(lambda x, y: x+y)
    count.pprint()

    """format data into df + ml on it"""

    ssc.start()
    ssc.awaitTermination()


if __name__ == "__main__":
    get_stream()