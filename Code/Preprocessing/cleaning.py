from datetime import datetime
import numpy as np
import pandas as pd
import heartpy as hp
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T
import matplotlib.pyplot as plt
from .formatting import index_to_time


def initialize_spark():
    return SparkSession \
        .builder \
        .appName("Spark session Data Engineering") \
        .config("spark.jars", '/bd-fs-mnt/General-Sparks/acacia_s3/*') \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

# ========= CODE AND FUNCTIONS ========= #
def clean_wavesample(df):
    """ Remove flatlines from the data """
    
    cleanWS = []
    cleanTS = []
    lens = []
    for row in range(len(df)):
        newWS = []
        newTS = []
        wsRow = df.iloc[row]['WaveSamples']
        
        for sam in range(len(wsRow)):
            wss = wsRow[sam]
            if wss != '0020' * int((len(wss)/4)) and wss != '0000' * int((len(wss)/4)):
                newWS.append(wss)
                newTS.append(df.iloc[row]['Timestamps'][sam])
        
        cleanWS.append(newWS)
        cleanTS.append(newTS)
    
    df['Timestamps'] = cleanTS
    df['WaveSamples'] = cleanWS
    
    
    return df

def combine_timestamps(df):
    """ Combining the data if the sequences follow each other immediately. """
    
    new_comb_ts = []
    new_comb_ws = []
    lens = []
    format_date = "%Y-%m-%d %H:%M:%S.%f %z" 
    for i in range(len(df)):
        row = df.iloc[i]
        print('start row '+str(i))
        
        # Not necessary if there is only one sample
        if len(row['Timestamps']) == 1:
            new_comb_ts.append(row['Timestamps'])
            new_comb_ws.append(row['WaveSamples'])
            lens.append(1)
            continue
        
        comb_ts = []
        comb_ws = []
        
        for t in range(len(row['Timestamps'])):
            if t == 0:
                comb_ts.append(row['Timestamps'][t])
                comb_ws.append(row['WaveSamples'][t])
            
            else:
                
                diff = datetime.strptime(row['Timestamps'][t], format_date) - datetime.strptime(row['Timestamps'][t-1], format_date)
                if diff.total_seconds() == 5.12:
                    comb_ws[-1] += row['WaveSamples'][t]
                
                else:
                    comb_ts.append(row['Timestamps'][t])
                    comb_ws.append(row['WaveSamples'][t])
        
        new_comb_ts.append(comb_ts)
        new_comb_ws.append(comb_ws)
        lens.append(len(comb_ts))
        
        
    
    df['Timestamps'] = new_comb_ts
    df['WaveSamples'] = new_comb_ws
    df['Number_Samples'] = lens
    print('Successfully summarized')
    
    return df

def split_flatlines(df):
    # Pid, Label, Timestamps, WaveSamples, Number_Samples
    
    row_fl_len = []
    row_fl_sta = []
    row_val_ws = []
    row_val_st = []
    

    print(len(df))
    # 1. Loop over all rows (unique patient, label combis)
    for n in range(len(df)): 
        partial = df.iloc[n]
        print("New row with "+str(partial['Number_Samples'])+" wavesamples")
        
        # Creeer rij specifieke lijsten voor de flatlines en échte sequences
        fl_lengths = []
        fl_starts = []
        valid_wavesamples = []
        valid_wavestarts = []
        
        # 2. Loop over all WaveSamples (Number_Samples)
        st = datetime.now()

        for m in range(partial['Number_Samples']):
            wavesample = partial['WaveSamples'][m]
            timestamp = partial['Timestamps'][m]
            size = round(len(wavesample)/4)

            
            # 3. Loop over the string in character pairs of four
            start_rec = 0
            len_flat = 0
            
            for k in range(size):
                start = k * 4
                end = start + 4
                value = wavesample[start:end]
                
                # 4. Check the value in the string
                if value in ['0000', '0020'] and k != size - 1:
                    if len_flat == 0:
                        start_flat = start #store the starting index
                        
                    len_flat += 1
                    
                # 5. What to do at the end of the flatline?
                else:
                    
                    if len_flat < 10:
                        len_flat = 0
                            
                    else: #Flatline gespot!
                        
                        # a. Krijg het eindpunt van de flatline
                        end_flat = start #letterlijk ook het startpunt van de volgende 
                        start_flat_time = index_to_time(start_flat, timestamp)
                        
                        # b. Sla de lengte en startpunt van de flatline op in twee lijsten
                        fl_lengths.append(len_flat)
                        fl_starts.append(start_flat_time)
                        
                        # c. Splits de waveform af voordat de flatline begint --> Aparte sequence met starttijd
                        end_rec = start_flat - 1 #eentje terug
                        
                        if end_rec > start_rec:
                            valid_ws = wavesample[start_rec: end_rec]
                            start_rec_time = index_to_time(start_rec, timestamp)

                            valid_wavestarts.append(start_rec_time)
                            valid_wavesamples.append(valid_ws)
                        
                        start_rec = end_flat
                        len_flat = 0

        row_fl_len.append(fl_lengths)
        row_fl_sta.append(fl_starts)
        row_val_ws.append(valid_wavesamples)
        row_val_st.append(valid_wavestarts)

    df['Timestamps'] = row_val_st
    df['WaveSamples'] = row_val_ws
    df['Flatline_Starts'] = row_fl_sta
    df['Flatline_Lengths'] = row_fl_len
    
    en = datetime.now()
    print(en-st)
        
    return df

def weighted_moving_average(ecg, sigma = 2, M = 10):
    
    weights = np.exp(-(np.arange(M) - (M - 1) / 2 )**2 / (2 * sigma **2))
    weights /= np.sum(weights)
    
    return np.convolve(ecg, weights, mode='valid')

def preprocessing_waveform(df, df_wf, label:int, index=0, low=0.75, high=6.5):
    """ 
    
    The processes of translating and cleaning a waveform.
    
    PARAMS
    ========
    * df: pd.DataFrame - The dataframe with the wavesamples for that patient.
    * label: int - an integer that represents the label that you want, this is different for each patient.
    * index: int (default 0) - which of the recording periods do you want to analyse? 
    * df_wf: pd.DataFrame (default df_wf) - The dataframe that represents the measuring instruments.
    * low: int (default 0.75) - The cut-off of the low frequency of the noise.
    * high: int (default 6.5) - The cut-off of the high frequency of the noise.
    
    RETURNS
    ========
    * clean_wave_sample: list(int) - A list with the cleaned waveform values.
    
    """
    
    wave_sample = df.iloc[label]['WaveSamples'][index]
    pid = df.iloc[label]['PatientID']
    label = df.iloc[label]['Label']
    
    translated_wave_sample = translate_WaveSample(wave_sample, pid, label, df_wf)
    clean_wave_sample = denoise(translated_wave_sample, low, high)
    
    return clean_wave_sample

def ecg_invert(ecg: list):
    """**ECG signal inversion**

    Neurokit: Checks whether an ECG signal is inverted, and if so, corrects for this inversion.
    To automatically detect the inversion, the ECG signal is cleaned, the mean is subtracted,
    and with a rolling window of 2 seconds, the original value corresponding to the maximum
    of the squared signal is taken. If the median of these values is negative, it is
    assumed that the signal is inverted.

    """
    # Check if the signal is inverted
    ecg_meanzero = ecg - np.nanmean(ecg)
    x_rolled = np.lib.stride_tricks.sliding_window_view(ecg_meanzero, 2000, axis=0)
    shape = np.array(x_rolled.shape)
    shape[-1] = -1
    max_squared = np.take_along_axis(x_rolled, np.square(x_rolled).argmax(-1).reshape(shape), axis=-1)
    med_max_squared = np.nanmedian(max_squared)
    
    # If it is inverted, change back
    if med_max_squared < 0:
        was_inverted = True
        ecg = np.array(ecg) * -1 + 2 * np.nanmean(ecg)
    else:
        was_inverted = False

    return ecg, was_inverted
                                   

# ======= INTERNAL FUNCTIONS ======= #

def translate_WaveSample(WS: str, PID: str, lab: str, df_measurement):
    """ Transform WaveSamples to actual values """
    WaveSample = WS
    patientID = PID
    label = lab
    
    # Generate the correct information from the measurement table
    ms_info = df_measurement[ ( df_measurement['PatientId'] == patientID ) & ( df_measurement['Label'] == label)]
    ms_info = ms_info.iloc[0]
    
    scale_upper = float(ms_info['CalibrationScaledUpper'])
    scale_lower = float(ms_info['CalibrationScaledLower'])
    abs_upper = float(ms_info['CalibrationAbsUpper'])
    abs_lower = float(ms_info['CalibrationAbsLower'])
    
    # Reform the waveSample
    ws_data = WaveSample.replace('0x', '')
    wave_split = np.array([ws_data[j:j+2] for j in range(0, len(ws_data), 2)])
    wave_reorder = [wave_split[j] for j in np.matrix([range(1,len(wave_split),2),range(0,len(wave_split),2)]).flatten('F')]
    
    # Compute the values
    wave_sample_dec = np.array([int(wave_reorder[0][0][j*2]+wave_reorder[0][0][j*2+1], 16) for j in range(0,len(wave_reorder[0][0])//2)])
    
    abs_diff = abs_upper - abs_lower
    scale_diff = scale_upper - scale_lower
    values = np.around(np.multiply(wave_sample_dec, float((abs_diff / scale_diff))) + float((abs_upper - abs_diff / scale_diff * scale_upper)),3).tolist()

    return np.array( values + [0]*(int(5120/2) - len(values)) )


def denoise(values, low: float, high: float):
    """ 

    Denoising method to reduce the electronic noise using Butterworth filtering.

    PARAMS
    ==========
    * sample: Signal -- the ECG signal as a Signal class form.
    * low: float -- cut-off of the low frequency of noise.
    * high: float -- cut-off of the high frequency of noise.

    RETURNS
    ==========
    * sample: Signal -- the ECG signal with reduced noise.

    """
    
    freq = 500

    # Filter baseline wander
    filtered = hp.filter_signal(values, cutoff = [low, high], sample_rate = freq, filtertype='bandpass')
    filtered = hp.filter_signal(filtered, cutoff = low, sample_rate = freq, filtertype='highpass')

    return filtered

def normalize(values):
    return np.array( [ (val - np.min(values) )/(np.max(values) - np.min(values) ) for val in values] )