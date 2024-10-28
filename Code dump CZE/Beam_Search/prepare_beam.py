"""
Copy of the code for "Exceptional Model Mining for Repeated Cross-Sectional Data (EMM-RCS)" 
by R. Schouten, W. Duivesteijn, and M. Pechenizkiy, 
accepted for publication at SIAM International Conference on Data Mining 2022 (SDM).

"""

import numpy as np
import pandas as pd

def collect_beam_and_candidate_result_set(candidate_result_set=None, cq_satisfied=None, w=None):

    n_redun_descs = None
    if len(cq_satisfied) > 0:
        candidate_result_set, candidate_queue = prepare_beam_and_candidate_result_set(candidate_result_set=candidate_result_set, 
                                                                                                         cq_satisfied=cq_satisfied, w=w)
    else:
        candidate_queue = []

    return candidate_result_set, candidate_queue


def prepare_beam_and_candidate_result_set(candidate_result_set=None, cq_satisfied=None, w=None):
   
    cq_sorted = sorted(cq_satisfied, key = lambda i: i[1]) #Sort based on the quality
    
    selected_for_result_list = cq_sorted[0:w]
    candidate_result_set.append(selected_for_result_list) # creates a nested list
    rs_candidates = [item for sublist in candidate_result_set for item in sublist] # unlist all elements

    return [rs_candidates], cq_sorted