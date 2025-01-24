import Simulation.loaddata as ld
import Code.Feature_Extraction.PQR_delineate as fe

import os
import re
from natsort import natsorted
import datetime

def generate_features(data_name=None, model_params=None, max_i=None):
    """ Extract the features from the ECGs and put them into a new database. """

    # Get the right directory
    if data_name == 'CPSC2021':
        filepath = 'Data/CPSC2021'
    else:
        return "Fault: Unknown dataset."

    # Get the individual records
    sample_set = open(os.path.join(filepath, 'RECORDS'), 'r').read().splitlines()
    sorted_set = natsorted(sample_set)
    
    pids = []
    feats = {}
    i = 0
    pid_prev = 'placeholder'

    for record in sorted_set:
        if i == max_i:
            return feats
        i += 1
        
        pid = re.search(r'data_(\d+)_', record).group(1)
        wid = re.search(r'_(\d+)$', record).group(1)
        if pid != pid_prev:
            print(f"Start on pid={pid} at ", str(datetime.datetime.now()))
        
        pid_prev = pid

        kernelerror = ['8', '11', '25', '38', '40', '51', '57', '71', '50']
        if pid in kernelerror:
            continue
        
        
        leadII, af_bin = ld.load_record(data_name, record)

        if pid in pids:
            avg_PQ = avg_PQ
            avg_count = avg_count
        else:
            avg_PQ = None
            avg_count = None 

        try:
            extra_features, avg_PQ, avg_count = fe.extract_features(leadII, pid, wid, avg_PQ = avg_PQ, avg_count = avg_count, model_params=model_params)
            pids.append(pid)
            extra_features['AF'] = af_bin  

            feats = { key: feats.get(key, []) + extra_features.get(key, []) for key in set(list(feats.keys()) + list(extra_features.keys())) }

        except:
            print('skipped')
        

    return feats