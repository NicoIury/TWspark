from pyspark.sql import *
from pyspark.sql.types import *

from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression, NaiveBayes
from pyspark.ml.feature import HashingTF, Tokenizer, IDF, StringIndexer
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator

from os import path


INPUT_DATA = "/home/nico/Nico/pyProg/projData/training.1600000.processed.noemoticon.csv"
MODEL_PATH = "/home/nico/Nico/pyProg/Big_data_2p/TWspark/model"


def model_gen():
    spark = SparkSession.builder.appName("p1").getOrCreate()
    df_schema = StructType([StructField("target", IntegerType(), True),
                            StructField("id",  IntegerType(), True),
                            # dataType usabile here
                            StructField("date", StringType(), True),
                            StructField("flag", StringType(), True),
                            StructField("user", StringType(), True),
                            StructField("text", StringType(), True)])

    df = spark.read.format("csv")\
        .option("header", "false")\
        .schema(df_schema)\
        .option("delimiter", ",")\
        .load(INPUT_DATA)

    # pulire dati dal df aka: encoding html tag (bs?), eliminare @, eliminare url e set tutto minusc

    df = df.drop("id", "date", "flag", "user")

    """clean dataFrame"""
    # clean_df(df)

    # df split: training (90%), test (10%)
    (training_df, test_df) = df.randomSplit([0.90, 0.10])
    # test_df = test_df.drop("target")

    """pipeline components"""
    tokenizer = Tokenizer(inputCol="text", outputCol="words")
    # splitted_df = tokenizer.transform(df)

    hashing = HashingTF(inputCol="words", outputCol="term_freq", numFeatures=2**16)
    # featurized_data = hashingTF.trasform(splitted_df)

    idf = IDF(inputCol="term_freq", outputCol="features", minDocFreq=5)

    # map target 0 (neg) to label 0.0, and target 4 (pos) to label 1.0
    target_to_label = StringIndexer(inputCol="target", outputCol="label")

    # lr = LogisticRegression(featuresCol="features", labelCol="label",  maxIter=100)
    nb = NaiveBayes(smoothing=1.0, modelType="multinomial")

    """pipeline and model"""
    pipeline = Pipeline(stages=[tokenizer, hashing, idf, target_to_label, nb])
    model = pipeline.fit(training_df)

    """prediction on test dataset"""
    pred = model.transform(test_df)
    # pred.show()

    """model evaluation section"""
    eval_prediction(pred)

    """save model"""
    save_model(model)

    """
    # lr:
    eval = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction")
    print(eval.evaluate(pred))
    
    # alternativa
    acc = pred.filter(pred.label == pred.prediction).count() / float(test_df.count())
    print(acc)
    """


def save_model(model):
    model.save(path.join(MODEL_PATH, "pipe_model"))


def eval_prediction(pred):
    eval = MulticlassClassificationEvaluator(labelCol="label",
                                             predictionCol="prediction",
                                             metricName="f1")
    print(eval.evaluate(pred))


def clean_df(df):
    pass


if __name__ == "__main__":
    model_gen()


