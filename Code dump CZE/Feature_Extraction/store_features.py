# ========= SETUP IMPORTANT FEATURES ========= #
import sys
from os import popen, listdir
from pathlib import Path
from Preprocessing.formatting import data_reformatting
from Preprocessing.cleaning import combine_timestamps, translate_WaveSample, denoise, weighted_moving_average, split_flatlines
from Feature_Extraction.PQR_delineate import extract_features
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import heartpy as hp
#pio.renderers.default = 'browser'


directory = '/bd-fs-mnt/acacia-working-area/dwc/lieke/'

def initialize_spark():
    return SparkSession \
        .builder \
        .appName("Spark session Data Engineering") \
        .config("spark.jars", '/bd-fs-mnt/General-Sparks/acacia_s3/*') \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

# ========== ACTUAL CODE ========= #
def get_measurements():
    
    read_path = '/bd-fs-mnt/acacia-landing-zone/dwc/sn002_Frederique/dobutamine_OK/'
    spark = initialize_spark()
    
    df_wf = spark.read.format('delta').load(read_path + 'Wave')\
        .select('PatientId', 'Label', 'CalibrationScaledLower', 'CalibrationScaledUpper', 'CalibrationAbsLower', 'CalibrationAbsUpper', 'ScaleLower', 'ScaleUpper')\
        .filter(F.col('Label').isin(['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6'])).dropDuplicates().toPandas()
    
    return df_wf

def store_flatlines(PID: str):

    df = pd.read_parquet('/bd-fs-mnt/acacia-working-area/dwc/lieke/Data/PID='+PID+'.parquet')
    print('df openened')
    df = combine_timestamps(df)
    df = split_flatlines(df)
    
    return df


def store_features(PID: str, plot=False):
    # Features are only selected based on lead II
    wished_labels = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
    
    #df_measurements = get_measurements()

    df = pd.read_csv('/bd-fs-mnt/acacia-working-area/dwc/lieke/Data2/PID='+PID+'.csv')

    return df[df['Label'] == 'II']
    """
    # Loop over each wavesample heen en translate dan pas (niet permanent!)
    #times = df.iloc[0]['Timestamps']
    wavesamples = df.iloc[0]['WaveSamples']
    print(len(wavesamples))
    
    for w in [2]:
        

        print(wavesamples[w])
        ecg = translate_WaveSample( wavesamples[w], PID.upper(), 'II', df_measurements)[:100000]
        print(ecg)
        #filtered = hp.filter_signal(ecg, cutoff = [0.5, 11], sample_rate = 500, filtertype='bandpass')
        filtered = weighted_moving_average(ecg, M=30, sigma=500)
        
        
        plt.figure(figsize=(24,8))
        plt.plot(ecg, label='ECG')
        plt.plot(filtered, label='Filtered')
        plt.legend()
        plt.show()
        

        feats = extract_features(filtered) #now in ID format.
        print(feats)
        
        plt.figure(figsize=(24, 8))
        #plt.plot(ecg, label='Original ECG', size=2)
        plt.plot(filtered , label='Filtered ECG')
        #plt.scatter(feats['R-peak'], ecg[feats['R-peak']], color='red', label='R-peaks')
        plt.scatter(feats['R-peak'], filtered[feats['R-peak']], color='red', label='R-peaks')
        plt.scatter(feats['P-wave'], filtered[feats['P-wave']], color='lightgreen', label='P-wave')
        #plt.scatter(feats['Waves'], ecg[feats['Waves']], color='green')
        #plt.scatter(feats['P_onset'], filtered[feats['P_onset']], color='lightgreen', label='P_onset')
        #plt.scatter(feats['P_offset'], filtered[feats['P_offset']], color='lightgreen', label='P_offset')
        for i in range(len(feats['P_onset'])):
            plt.axvspan(feats['P_onset'][i], feats['P_offset'][i], color='lightgreen', alpha=0.2)
        plt.legend()
        plt.show()

        """
    #return feats

