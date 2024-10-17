# This file contains all functions needed to open, load, and save the ECG from any of the included public datasets.
import wfdb
import os
import matplotlib.pyplot as plt

def open_files(dataset="CPSC"):
    """
    The data is saves per instance. This opens the file for one such instance.
        .atr = ...
        .hea = header file
        .dat = binary data file

    Input:
    * dataset (str): the dataset that will be used.
    """

    if dataset == 'CPSC':
        filepath = 'Data/CPSC2021'
    elif dataset == 'MITBIH' or dataset == 'MIT-BIH':
        filepath = 'Data/MIT-BIH'
    else:
        return "Fault: Unknown dataset."
    

    sample_set = open(os.path.join(filepath, 'RECORDS'), 'r').read().splitlines()
    for i, sample in enumerate(sample_set):
        sample_path = os.path.join(filepath, sample)

        ecg, info = load_data(sample_path)
        print(ecg)
        print(info)

        # Keep only the lead II data
        #ecg_II = [value[1] for value in ecg]

        if i == 10:
            return "10 done"
        #save_dict(os.path.join(RESULT_PATH, sample+'.json'), pred_dict)
    
    return "done"

def load_data(path: str):
    ecg, info = wfdb.rdsamp(path)

    return ecg, info


