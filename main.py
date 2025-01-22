import pandas as pd
import ast
from collections import Counter

import Code.Beam_Search.beam_search as bs
import Simulation.EHR_sensitive as ehr
from Simulation.loaddata import aggregate_dataset
from Simulation.extract_feats import generate_features
from Code.Analysis.compute_qualitymeasures import compute_qualitymeasures
from Code.Analysis.postprocessing import resultset_table

def main(save_location=None, data_name=None, beam_params=None, model_params=None, date=None, descriptor_location=None, target_location=None, evaluator_location=None, tasks=None):
    """
    The output is a dataframe.
    """

    # Generate the synthetic EHR if that is wanted
    if tasks['generate_EHR']:
        EHR = ehr.generate_EHR(data_name = data_name)
        EHR.to_csv(save_location + 'processed/EHR_' + date +'.csv')
    
    else:
        EHR = pd.read_csv(descriptor_location)
    
    # Generate the features from the input ECG
    if tasks['compute_qualitymeasures']:
        ECG_dict = generate_features(data_name, model_params)
        ECG_features = pd.DataFrame.from_dict(ECG_dict)

        ECG_features = aggregate_dataset(ECG_features)

        # Compute AF instances
        nonAF, AF = [], []
        for row in range(len(ECG_features)):
            pat = ECG_features.iloc[row]
            cs = Counter( ast.literal_eval(pat['AF']))

            if cs['persistent atrial fibrillation'] != 0 or cs['paroxysmal atrial fibrillation'] != 0:
                AF.append(1)
            else:
                nonAF.append(0)
        
        AF_complications = pd.DataFrame({'PID': range(len(ECG_features)), 'AF': AF, 'Non AF': nonAF})

        # Compute quality measures
        quality_measures = compute_qualitymeasures(features = ECG_features)

        AF_complications.to_csv(save_location + 'processed/AF_complications' + date + '.csv', index=False) 
        quality_measures.to_csv(save_location + 'processed/quality_measures' + date + '.csv', index=False) 

    else:
        quality_measures = pd.read_csv(target_location)
        AF_complications = pd.read_csv(evaluator_location)

    # Perform beam search
    result_emm = bs.beam_search(descriptors = EHR, 
                               targets = quality_measures, 
                               evaluators = AF_complications, 
                               phenotype = model_params['phenotype'], 
                               q = beam_params['q'], w = beam_params['w'], 
                               d = beam_params['d'], b = beam_params['b'], 
                               cp = beam_params['cp'])

    result_table = resultset_table(result_emm, model_params)
    result_table.to_csv(save_location + 'output/result_' + model_params['phenotype'] + '_' + date + '.csv', index=False)
    
    return result_table



if __name__ == '__main__':

    # Frequency (freq) is measured in Hz
    # Options for phenotype: SDSD, RMSSD, SDRR, P-count, F-count, SDSD_P, RMSSD_P, SDRR_P, SDSD_F, RMSSD_F, SDRR_F

    main(
        save_location = 'Data/',
        data_name = 'CPSC2021',
        beam_params = {'cp': 0.05, 'w': 50, 'd': 3, 'b': 3, 'q': 2},
        model_params = {'freq': 200, 'phenotype': 'SDSD_P', 'cutoff': 0.75, 'sigma': 20, 'M': 10},
        date = '20250122',
        descriptor_location = None, #csv file
        target_location = None,
        evaluator_location = None,
        tasks = {'generate_EHR': True, 'compute_qualitymeasures': True}
    )

    """
    main(
        save_location = 'Data/',
        data_name = 'CPSC2021',
        beam_params = {'cp': 0.05, 'w': 50, 'd': 3, 'b': 3, 'q': 2},
        model_params = {'freq': 200, 'phenotype': 'SDSD_P'},
        date = '20250122',
        descriptor_location = None, #csv file
        target_location = None,
        evaluator_location = None,
        tasks = {'generate_EHR': True, 'compute_qualitymeasures': True}
    )
    """
