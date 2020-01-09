from pyspark.sql import *
from pyspark.sql.types import *
import pyspark.sql.functions as f

#import numpy

from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression, NaiveBayes
from pyspark.ml.feature import HashingTF, Tokenizer, IDF, StringIndexer
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator

from os import path

IN_PATH = "/Users/valentino_milia/Desktop/II Project - BIG DATA/training.1600000.processed.noemoticon.csv"
MODEL_PATH = "/Users/valentino_milia/PycharmProjects/Clear_DB/model"


def blank_as_null(x):
    return f.when(f.col(x) != "", f.col(x)).otherwise(None)

def save_model(model):
    model.save(path.join(MODEL_PATH, "pipe_model"))


def eval_prediction(pred):
    eval = MulticlassClassificationEvaluator(labelCol="label",
                                             predictionCol="prediction",
                                             metricName="f1")
    print(eval.evaluate(pred))



def model_gen():
    regex = r"((https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b)|([^A-Za-z0-9 '!?.:,;ìàòèéù])"

    spark = SparkSession.builder.appName("Script_CleanDB").getOrCreate()
    df_schema = StructType([StructField("target", IntegerType(), True),
                            StructField("id", IntegerType(), True),
                            # dataType usabile here
                            StructField("date", StringType(), True),
                            StructField("flag", StringType(), True),
                            StructField("user", StringType(), True),
                            StructField("text", StringType(), True)])

    tweeter_DF = spark.read.format("csv")\
        .option("header", "false")\
        .schema(df_schema)\
        .option("delimiter", ",")\
        .option("mode", "DROPMALFORMED")\
        .load(path.join(IN_PATH))

    #Elimino righe con text vuoti
    tweeter_DF = tweeter_DF.withColumn("text", blank_as_null("text"))
    tweeter_DF.na.drop()

    #Pulisco il csv
    tweeter_DF = tweeter_DF.withColumn("text", f.regexp_replace(f.col("text"), regex, ''))

    # Salvo il DataFrame pulito
    tweeter_DF.show()
    tweeter_DF.write.csv('/Users/valentino_milia/Desktop/II Project - BIG DATA/Output_DB.csv', mode="overwrite")

    #Elimino campi inutili
    tweeter_DF = tweeter_DF.drop("id", "date", "flag", "user")

    #DF split: training (90%), test (10%)
    (training_df, test_df) = tweeter_DF.randomSplit([0.90, 0.10])

    """pipeline components"""
    tokenizer = Tokenizer(inputCol="text", outputCol="words")

    hashing = HashingTF(inputCol="words", outputCol="term_freq", numFeatures=2 ** 16)

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

    """End spark process"""
    spark.stop()


model_gen()