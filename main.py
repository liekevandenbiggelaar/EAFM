import pandas as pd
import datetime

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
    
    start = datetime.datetime.now()
    print(start)

    # Generate the features from the input ECG
    if tasks['compute_qualitymeasures']:
        ECG_dict = generate_features(data_name, model_params)
        ECG_features = pd.DataFrame.from_dict(ECG_dict)

        ECG_features = aggregate_dataset(ECG_features)

        # Compute AF instances
        AF = []
        for row in range(len(ECG_features)):
            pat = ECG_features.iloc[row]

            if 'persistent atrial fibrillation' in pat['AF'] or 'paroxysmal atrial fibrillation' in pat['AF']:
                AF.append(1)
            else:
                AF.append(0)
        
        AF_complications = pd.DataFrame({'PID': ECG_features['PID'], 'AF': AF})

        # Compute quality measures
        quality_measures = compute_qualitymeasures(features = ECG_features)

        AF_complications.to_csv(save_location + 'processed/AF_complications_' + date + '.csv', index=False) 
        quality_measures.to_csv(save_location + 'processed/quality_measures_' + date + '.csv', index=False) 
        target_location = save_location + 'processed/AF_complications_' + date + '.csv'
        evaluator_location = save_location + 'processed/quality_measures_' + date + '.csv'

    quality_measures = pd.read_csv(target_location)
    AF_complications = pd.read_csv(evaluator_location)



    # Generate the synthetic EHR if that is wanted
    if tasks['generate_EHR']:
        EHR = ehr.generate_EHR(data = quality_measures)
        EHR.to_csv(save_location + 'processed/EHR_' + date +'.csv')
        descriptor_location = save_location + 'processed/EHR_' + date +'.csv'

    EHR = pd.read_csv(descriptor_location)


    # Perform beam search
    result_emm = bs.beam_search(descriptors = EHR.set_index('PID'), 
                               targets = quality_measures.set_index('PID'), 
                               evaluators = AF_complications.set_index('PID'), 
                               phenotype = model_params['phenotype'], 
                               q = beam_params['q'], w = beam_params['w'], 
                               d = beam_params['d'], b = beam_params['b'], 
                               cp = beam_params['cp'])
    

    result_table = resultset_table(result_emm, model_params, beam_params, AF_complications) #result EMM is empty
    result_table.to_csv(save_location + 'output/result_' + model_params['phenotype'] + '_' + date + '.csv', index=False)

    end = datetime.datetime.now()
    print(start)
    print(end)
    print(end - start)
    
    return result_emm



if __name__ == '__main__':

    # Frequency (freq) is measured in Hz
    # Options for phenotype: SDSD, RMSSD, SDRR, P-count, F-count, SDSD_P, RMSSD_P, SDRR_P, SDSD_F, RMSSD_F, SDRR_F
    # Locations must be in the form of a csv file
    # if another data source will be used, change the data_name, and add the data loading necessary for this source in the Simulation/loaddata.py file
    # The current setup is run on the generated data sets which are included in the repository. One can run this again with feature extraction but this takes longer

    # This version runs all experiments, saving them in separate locations.
    for thet in ['SDSD', 'RMSSD', 'SDRR', 'P-count', 'F-count', 'SDSD_P', 'RMSSD_P', 'SDRR_P', 'SDSD_F', 'RMSSD_F', 'SDRR_F']:
        main(
            save_location = 'Data/',
            data_name = 'CPSC2021',
            beam_params = {'cp': 0.05, 'w': 50, 'd': 3, 'b': 5, 'q': 1},
            model_params = {'freq': 200, 'phenotype': thet, 'cutoff': 0.75, 'sigma': 20, 'M': 10},
            date = '20250123',
            descriptor_location = 'Data/processed/EHR_20250123.csv', #csv file
            target_location = 'Data/processed/quality_measures_20250123.csv', #csv file
            evaluator_location = 'Data/processed/AF_complications_20250123.csv', #csv file
            tasks = {'generate_EHR': False, 'compute_qualitymeasures': False} 
        ) 

# This version takes about 15 seconds to run completely.
# It uses the processed data sets from the repository
"""
    main(
        save_location = 'Data/',
        data_name = 'CPSC2021',
        beam_params = {'cp': 0.05, 'w': 50, 'd': 3, 'b': 5, 'q': 1},
        model_params = {'freq': 200, 'phenotype': 'SDSD_P', 'cutoff': 0.75, 'sigma': 20, 'M': 10},
        date = '20250123',
        descriptor_location = 'Data/processed/EHR_20250123.csv', #csv file
        target_location = 'Data/processed/quality_measures_20250123.csv', #csv file
        evaluator_location = 'Data/processed/AF_complications_20250123.csv', #csv file
        tasks = {'generate_EHR': False, 'compute_qualitymeasures': False} 
    ) 
"""

# This version takes about 2 hours and 20 minutes to run completely.
# It does the processing again
"""
    main(
        save_location = 'Data/',
        data_name = 'CPSC2021',
        beam_params = {'cp': 0.05, 'w': 50, 'd': 3, 'b': 5, 'q': 1},
        model_params = {'freq': 200, 'phenotype': 'SDSD_P', 'cutoff': 0.75, 'sigma': 20, 'M': 10},
        date = '20250123',
        descriptor_location = None,
        target_location = None,
        evaluator_location = None,
        tasks = {'generate_EHR': True, 'compute_qualitymeasures': True} 
    ) 
"""

