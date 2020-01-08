import pyspark.sql.functions as f


def blank_as_null(x):
    return f.when(f.col(x) != "", f.col(x)).otherwise(None)


def clean_df(tweet_df):
    regex = r"((https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b)|([^A-Za-z0-9 '!?.:,;ìàòèéù])"
    tweet_df = tweet_df.withColumn("text", blank_as_null("text"))
    tweet_df.na.drop()
    tweeter_df = tweet_df.withColumn("text", f.regexp_replace(f.col("text"), regex, ''))

