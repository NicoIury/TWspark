#lettura del file json in Spark seguendo:

from all_path import JSON_FILE, MODEL_PATH, INPUT_FOLDER, DATASET_FILE, GENERATED_DF

from pyspark.sql import *

class DF:

    def create_df(path):
        print(f"[+] Creating Spark DF from {path}")
        spark = SparkSession.builder.appName("historical_tweets").getOrCreate()
        df = spark.read.option("multiLine", True).option("mode", "PERMISSIVE").json(path)
        df.show()
        #df.select("text").write.save(GENERATED_DF)
        return df

    def save_df(path, df):
        print(f"[*] Saving Spark DF in {path}")
        df.select( "text").write.save(path, format="parquet",mode="overwrite")
        print("End")

"""
if __name__ == "__main__":
    df=create_df(JSON_FILE)
    save_df(GENERATED_DF,df)
"""
