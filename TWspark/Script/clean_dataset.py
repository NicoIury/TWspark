import pyspark.sql.functions as f

import MLmodel

from os import path


def clean_df(df):
    print("[*] cleaning dataset...")
    regex = r"(http.\S+)|(@[^\s]+)"
    df = df.withColumn("text", f.lower(f.col("text")))
    df = df.withColumn("text", f.regexp_replace(f.col("text"), regex, ""))
    df = df.filter(df.text.isNotNull() & (df.text != ""))
    df.na.drop()

    df.write.csv(path.join(MLmodel.INPUT_FOLDER, "cleaned_df.csv"), mode="overwrite")
    print("[+] cleaning complete.")


if __name__ == "__main__":
    df = MLmodel.create_df()
    clean_df(df)
