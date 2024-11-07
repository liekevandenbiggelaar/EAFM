# This file contains all functions needed to open, load, and save the ECG from any of the included public datasets.
import wfdb
import os
import re


def load_record(dataset: str, record: str):

    # Get the right directory
    if dataset == 'CPSC':
        filepath = 'Data/CPSC2021'
    elif dataset == 'MITBIH' or dataset == 'MIT-BIH':
        filepath = 'Data/MIT-BIH'
    else:
        return "Fault: Unknown dataset."
    
    sample_path = os.path.join(filepath, record)

    found, ecg, info = load_ecg_info(sample_path)
        #print(sample_path)
    if found == False:
        return [], []
    else:
        leadII = ecg[:, 1]
        af_bin = info['comments']
    
        return leadII, af_bin

def load_ecg_info(path: str):
    try:
        ecg, info = wfdb.rdsamp(path)
        return True, ecg, info
    
    except:
        return False, [], []

    


