# Code for the extraction of features
import Simulation.loaddata as ld
import Code.Feature_Extraction.PQR_delineate as fe
#import Code.Feature_Extraction.store_features as sf
#import Code.Preprocessing as pr
#import Code.Analysis as an
#import Code.Beam_Search as bs

import pandas as pd
import os
import re
from natsort import natsorted

def generate_features(dataset='CPSC'):
    """ Extract the features from the ECGs and put them into a new database. """

    # Get the right directory
    if dataset == 'CPSC':
        filepath = 'Data/CPSC2021'
        rate = 200
    elif dataset == 'MITBIH' or dataset == 'MIT-BIH':
        filepath = 'Data/MIT-BIH'
        rate = 250
    else:
        return "Fault: Unknown dataset."

    # Get the individual records
    sample_set = open(os.path.join(filepath, 'RECORDS'), 'r').read().splitlines()
    sorted_set = natsorted(sample_set)
    
    pids = []
    feats = {}
    i = 0
    for record in sorted_set:
        i += 1

        pid = re.search(r'data_(\d+)_', record).group(1)
        wid = re.search(r'_(\d+)$', record).group(1)

        kernelerror = ['8', '11', '25', '38', '40', '51', '57', '71']
        if pid in kernelerror:
            continue
        
        print(f"Start on pid={pid} and wid={wid}")
        leadII, af_bin = ld.load_record(dataset, record)

        if pid in pids:
            avg_PQ = avg_PQ
            avg_count = avg_count
        else:
            avg_PQ = None
            avg_count = None 

        pids.append(pid)
        extra_features, avg_PQ, avg_count = fe.extract_features(leadII, pid, wid, avg_PQ = avg_PQ, avg_count = avg_count, rate=rate)
        extra_features['AF'] = af_bin  

        feats = { key: feats.get(key, []) + extra_features.get(key, []) for key in set(list(feats.keys()) + list(extra_features.keys())) }

    return feats