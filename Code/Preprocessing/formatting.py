from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T
from datetime import datetime, timedelta

def initialize_spark():
    return SparkSession \
        .builder \
        .appName("Spark session Data Engineering") \
        .config("spark.jars", '/bd-fs-mnt/General-Sparks/acacia_s3/*') \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.driver.memory", '100g') \
        .config("spark.driver.maxResultSize", 0) \
        .getOrCreate()

# ========= FILTER PARQUET FILE ========= #

def data_reformatting(PatientId: str, wished_labels: list):
    
    spark = initialize_spark()
    PatientId = PatientId.lower()
    
    return spark.read.format('avro').load('/bd-fs-mnt/acacia-landing-zone/dwc/sn002_Frederique/dobutamine_OK/' + "WaveSample/PID=" + PatientId) \
            .filter( (F.col('Label').isin(wished_labels)))\
            .withColumn('PatientId', F.lit(PatientId.upper())) \
            .select('PatientId', 'Timestamp', 'Label', 'WaveSample') \
            .sort("Label", "Timestamp") \
            .groupBy("PatientID", "Label") \
            .agg(F.collect_list("Timestamp").alias("Timestamps"), F.collect_list("WaveSample").alias("WaveSamples")).toPandas()

def save_as_file(df, title: str):
    
    save_path = '/bd-fs-mnt/acacia-working-area/dwc/lieke/Data/'
    df.to_parquet(save_path + "PID=" + title + ".parquet", compression='snappy')
    
    return 'Written to .parquet'

# ======= FILTER ON DATAFRAME ======== #
# Idee: PiD, Label, StartTimesWave, WaveSamples, StartTimesFlatline, LengthFlatlines

def index_to_time(ix: int, start):
    # each ix is 2 ms
    format_date = "%Y-%m-%d %H:%M:%S.%f %z"
    
    total_ms = ix * 2
    time_change = timedelta(milliseconds=total_ms) 
    date_str = datetime.strptime(start, format_date)
    index_time = str(date_str + time_change)
    return index_time