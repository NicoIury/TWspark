import pyspark.sql.functions as f

import MLtest

from os import path


def blank_as_null(x):
    return f.when(f.col(x) != "", f.col(x)).otherwise(None)


def clean_df(df):
    regex = r"((https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b)" \
            r"|([^A-Za-z0-9 '!?.:,;ìàòèéù])"
    df = df.withColumn("text", f.regexp_replace(f.col("text"), regex, ''))
    df = df.withColumn("text", blank_as_null("text"))
    df.na.drop()
    df = df.withColumn("text", f.lower(f.col("text")))
    df.write.csv(path.join(MLtest.INPUT_FOLDER, "cleaned_df.csv"), mode="overwrite")


if __name__ == "__main__":
    df = MLtest.create_df()
    clean_df(df)
