import numpy as np
import pandas as pd


def select_result_set(candidate_result_set=None, q=None):

    #print('result set selection')
    cq_sorted = sorted(candidate_result_set, key = lambda i: i[1]) #Sort based on the quality
    
    selected_for_result_list = candidate_queue[0:q]
    result_set.append(selected_for_result_list) # creates a nested list

    return result_set


def prepare_result_list(result_set=None):

    if len(result_set) == 0:
        
        print('Empty result set')
        result_emm = None
    
    else:        
        
        result_set_selected = result_set.copy()

        if len(result_set_selected) == 0:
            
            print('Empty result set')
            result_emm = None
        
        else: 

            result_emm = pd.DataFrame.from_dict(result_set_selected[0]).T
            result_emm.drop(columns=['sg_idx'], inplace=True)
            for sg in np.arange(1, len(result_set_selected)):
                new_sg = pd.DataFrame.from_dict(result_set_selected[sg]).T
                new_sg.drop(columns=['sg_idx'], inplace=True)
                result_emm = result_emm.append(new_sg)
            result_emm['sg'] = np.repeat(np.arange(len(result_set_selected)), 2) 
            result_emm.sort_index(axis=1, inplace=True)  

    return result_emm


