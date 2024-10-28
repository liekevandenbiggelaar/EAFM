from Preprocessing.cleaning import translate_WaveSample, weighted_moving_average, ecg_invert
from Feature_Extraction.store_features import store_features, get_measurements
from Feature_Extraction.PQR_delineate import extract_features
from Analysis.tables import create_metadata_table, add_metadata_table
import matplotlib.pyplot as plt
import os
import ast
import heartpy as hp
import pandas as pd

def get_wavesamples(pid: list):
    
    df_ws = store_features(pid)
    pid = pid.upper()
    df_measurement = get_measurements()
    df_m = df_measurement[df_measurement['PatientId'] == pid]
    wavesamples = ast.literal_eval(df_ws.iloc[0]['WaveSamples'])
    
    return wavesamples

def fill_metadata(patientIds: list):
    for pid in patientIds:
        
        if pid == patientIds[15]:
            continue
        
        metadata_finished = pd.read_csv('/bd-fs-mnt/acacia-working-area/dwc/lieke/MetadataTable.csv')
        wavesamples = get_wavesamples(pid)
        
        table_made = False
        i = 0
        for wavesample in wavesamples:
    
        wid = str(i)
    
        # It must at least have the recording length of 30 seconds, otherwise we can never identify AF
        if len(wavesample) < 4*500*30:
            i += 1
            continue

        else:
            print("Start wavesample "+ str(i))
            # Get the features and values
            ecg = translate_WaveSample( wavesample, pid, 'II', df_measurement )
            features = extract_features(ecg, pid, wid, short=False, plot=True)
            print("We got the features!")
    
            # Create the actual tables
            metadata2 = create_metadata_table(features, pid, wid)
    
            if table_made:
                # Concatenate for each wavesample
                tables = [metadata1, metadata2]
                metadata1 = add_metadata_table(tables)
        
            else:
                # No concatenation necessary
                metadata1 = metadata2
                table_made = True
     
            i+=1 #waveID
        
        tables = [metadata_finished, metadata1]
        metadata2 = add_metadata_table(tables)
        save_path = '/bd-fs-mnt/acacia-working-area/dwc/lieke/'
        metadata2.to_csv(save_path + "MetadataTable.csv", index=False)

    return metadata2
            
            
