import math

import Code.Beam_Search.refinements as rf
import Code.Beam_Search.select_subgroup as ss
import Code.Beam_Search.constraints as cs
import Code.Beam_Search.preprocess as pp
import Code.Beam_Search.qualitymeasure as qm
from Code.Beam_Search.priority_queue import PriorityQueue


def beam_search(epd, target, evaluation, theta: str, q: int, w: int, d: int, b: int, c: int):
    """
    Input
    =====
    epd: dataset containing information regarding the patients
    target: dataset containing the target attributes of the patients
    
    theta: choose the measurement value [SDSD, SDRR, RMSSD]
    q: number of subgroups that are wished
    w: maximum descriptions on a level
    d: maximum number of levels in the beam
    b: number of bins for the numeric refinement
    c: minimum subgroup size
    
    
    Output
    ======
    result_set: PriorityQueue of length (q) with the best q descriptions
    """
    
    # Get all the descriptive attributes and change to the right type
    attributes, descriptives = pp.define_attributes()
    epd = pp.define_dtypes(dataset=epd, descriptives=descriptives)
    
    # Create the candidate queue from all the features. This queue has unbouded length.
    candidate_queue = rf.create_starting_descriptions(dataset=epd, descriptives=descriptives, b=b)
    
    # Get the measurement average of the entire population.
    avg_theta_0 = qm.compute_theta(target_data=target, theta=theta, subgroup=epd)
    
    # Initialize the result set
    result_set = PriorityQueue(q, queue=[])
    
    # Loop over all levels of the beam search
    for lvl in range(1, d+1):
        
        beam = PriorityQueue(w, queue=[]) #store the best w of this level, start from scratch each level
        cq_satisfied = []
        
        # Loop over all descriptions in the candidate queue
        for seed in candidate_queue:
            
            if lvl == 1:
                # Use the candidate descriptions 
                seed_set = []
                seed_set.append(seed)
            else:                
                # Refine the candidate queue descriptions
                subgroup, idx_sg, subgroup_compl, idx_compl = ss.select_subgroup(description=seed['description'], df=epd, descriptives=descriptives)
                seed_set = rf.refine_seed(seed=seed, subgroup=subgroup, descriptives=descriptives, b=b)
                #print(seed_set)
            
            # Loop over all descriptions in the refined set
            for descr in seed_set:
                
                subgroup, idx_sg, subgroup_compl, idx_compl = ss.select_subgroup(description=descr['description'], df=epd, descriptives=descriptives)
                
                # It must be according to the conditions:
                # 1. The subgroup must be larger than c
                # 2. It must not be a similar description to what already exists
                # 3. The description must not be redundant
                if cs.satisfy_conditions(idx_sg, c, descr, cq_satisfied):
                    #print(descr, cq_satisfied)
                    
                    avg_theta_G = qm.compute_theta(target_data=target, theta=theta, subgroup=subgroup)
                    quality = qm.compute_qualitymeasure(avg_theta_G, avg_theta_0, idx_sg, idx_compl, evaluation, epd)
                    # In the insert of priority queues is also a check if there is not a more redundant value, if so, change
                    if not(math.isnan(quality)):
                        beam.insert((descr, quality, idx_sg))
                        #print(beam)
                        result_set.insert((descr, quality, idx_sg))
                        cq_satisfied.append(descr)
                    #print(result_set)
                #else:
                    #print('meh', idx_sg, descr)
        
        candidate_queue = beam.get_descriptions()
        #print(candidate_queue)
    
    return result_set.get_queue()
