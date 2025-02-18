import numpy as np
import pandas as pd

import Code.Beam_Search.preprocess as pp
import Code.Beam_Search.select_subgroup as ss

def resultset_table(result_tuple=None, model_params=None, beam_params=None, evaluators=None):

    

    resultsDct = {'Theta': [], 'Rank': [], 'Description': [], 'QM': [], 'AF Percentage': [], 'Indexes': []}

    resultsDct['Rank'] += [i for i in range(1, beam_params['q']+1)]
    resultsDct['Theta'] += [model_params['phenotype'] for i in range(0, beam_params['q'])]

    for res in result_tuple:
        resultsDct['Description'].append([res[0]])
        resultsDct['QM'].append(float(res[1]))
        resultsDct['Indexes'].append([int(i) for i in res[2]])

        evals = evaluators[evaluators['PID'].isin(res[2])]

        AFperc = np.array(evals['AF']).sum()/len(evals)
        resultsDct['AF Percentage'].append(AFperc)
        
    df_results = pd.DataFrame.from_dict(resultsDct)
    
    return df_results


def other_relations(result: int, results_dataset, patients_dataset, quality_dataset, af_dataset):
    """ 
    Code to check the relevance of all characteristics. 
    e.g. is x AND y AND z necessary or is x AND y also insightful? 
    """
    
    relations_dataset = pd.DataFrame()
    attributes, descriptives = pp.define_attributes()
    
    row = results_dataset.iloc[result]
    desc = eval(row['Description'])['description']
    theta = row['Theta']
    
    items = desc.items()

    temp = []
    # Get all items and its indexes
    for item in items:
        key = item[0]
        value = item[1]
        
        data_subgroup, ids = ss.select_subgroup(description=[key, value], df=patients_dataset, descriptives=descriptives)
        temp.append((str(key)+" "+str(value), ids))

    coms = [] + temp
    # Go over all combinations
    for i in range(len(temp)):
        for j in range(i, len(temp)):
            if i == j:
                continue
            
            d1 = temp[i][0]
            d2 = temp[j][0]
            
            i1 = set(temp[i][1])
            i2 = set(temp[j][1])
            i12 = i1 & i2
            
            d12 = d1 + " AND " + d2

            coms.append((d12, i12))
    
    # Get the one for the entire description
    d_all = ''
    i_all = set()
    for m in range(len(temp)):
        dm = temp[m][0]
        im = set(temp[m][1])
        if m == 0:
            d_all = dm
            i_all = im
        else:
            d_all += " AND " + dm
            i_all = i_all & im
    
    coms.append((d_all, i_all))
        
    
    relations_dataset['Description'] = [c[0] for c in coms]
    relations_dataset['Indexes'] = [c[1] for c in coms]
    
    # get average AF and phenotype difference
    af_lst = []
    qm_diff = []
    qm_perc = []
    
    for k in range(len(relations_dataset)):
        pats = list(relations_dataset.iloc[k]['Indexes'])
        pids = list(patients_dataset.iloc[pats]['PID'])
        
        compls = af_dataset[af_dataset['PID'].isin(pids)]
        nr_af = len(compls)
        af_perc = round(nr_af / len(pats) * 100, 2)
        
        af_lst.append(af_perc)
        
        qms = quality_dataset[quality_dataset['PID'].isin(pids)]
        theta_avg_group = round( np.mean(qms[theta]), 2)
        theta_avg_all = round( np.mean(quality_dataset[theta]), 2)
        theta_diff = round(theta_avg_group - theta_avg_all, 2)
        theta_diff_perc = round(theta_avg_group / theta_avg_all, 2)
        
        qm_diff.append(theta_diff)
        qm_perc.append(theta_diff_perc)
    
    relations_dataset['AF'] = af_lst
    relations_dataset['Pheno Diff'] = qm_diff
    relations_dataset['Pheno Diff %'] = qm_perc
    
    # get phenotype difference
    

     
    return relations_dataset
