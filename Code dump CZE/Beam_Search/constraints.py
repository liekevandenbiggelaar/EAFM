import numpy as np
import pandas as pd

# because the descriptions are saved in a dictionary
# it is possible to compare them without reordering them
# the binary, nominal (tuple), ordinal (Index) and numerical (tuple) can be handled
def similar_description(desc=None, cq_satisfied=None):

    check_similar_description = False

    # check for redundant descriptions (the exact same description but in another order)
    # the comparison has to be done with the candidate queue of the current iteration only
    # this queue is saved in cq_satisfied
    # in theory, a refinement at the current level can be similar to a desc from an earlier level
    # this can happen for numerical and ordinal attributes
    # changes are low that those descriptions will end up in the result list together
    for seed in cq_satisfied:
        if desc['description'] == seed['description']:
            #print(desc, seed)
            check_similar_description = True
            break

    return check_similar_description


def sufficient_subgroup_size(idx_sg: list, c: int):
    return len(idx_sg) >= c




def remove_redundant_descriptions(queue=None, descr=None):

    new_desc = descr
    
    redundancy_found = False #Start with nothing, only change if something if found
    best_descr, idx_descr = None, None
    
    i = 0
        
    for old_desc in queue: #We have already considered them
        if new_desc[1] == old_desc[1]:
            best_descr = compare_two_descs(old_desc=old_desc[0], new_desc=new_desc[0])
                    
            if best_descr == 'old_desc':
                #print('old', old_desc, new_desc)
                idx_descr = i
                redundancy_found = True
                        
            elif best_descr == 'new_desc':
                #print('new', old_desc, new_desc)
                idx_descr = i
                redundancy_found = True
            
            else:
                continue
        else:
            continue
                    
        i += 1

    return redundancy_found, best_descr, idx_descr


def compare_two_descs(old_desc=None, new_desc=None):

    length_dif = len(new_desc) - len(old_desc)

    best_descr = None
    if np.abs(length_dif) > 1:
        best_descr = None

    # new_desc is smaller than old_desc
    # check if all items exist in old_desc
    # if so, the new_desc is a general description/subset of old_desc
    elif length_dif == -1:
        items_exist_in_old_desc = [item in list(old_desc.items()) for item in list(new_desc.items())]
        #print('items_exist_in_old_desc', items_exist_in_old_desc)
        if np.all(items_exist_in_old_desc):
            best_descr = 'new_desc'

    # old_desc is smaller than new_desc
    # same procedure
    elif length_dif == 1:
        items_exist_in_new_desc = [item in list(new_desc.items()) for item in list(old_desc.items())]
        #print('items_exist_in_new_desc', items_exist_in_new_desc)
        if np.all(items_exist_in_new_desc):
            best_descr = 'old_desc'

    # check difference
    # if two or more keys are different, both can be kept
    # if two or more literals are different, both can be kept
    # otherwise, take the more general description
    elif length_dif == 0:
        same_keys = [key not in list(old_desc.keys()) for key in list(new_desc.keys())]
        #print('same_keys', same_keys)
        if np.sum(same_keys) < 2:
            same_descs = [item not in list(old_desc.items()) for item in list(new_desc.items())]
            #print('same_descs', same_descs)
            if np.sum(same_descs) == 1:
                # we know the difference is in the key difference, we remove the latest one
                best_descr = 'old_desc'
            elif np.sum(same_descs) == 0:
                # remove the more general description
                # bit complex to write, for convenience we remove the latest one
                best_descr = 'old_desc'
            else: 
                best_descr = None

    else:
        print('some mistake, new subgroup is larger than old subgroup')
        best_descr = None

    #print('remove', remove)

    return best_descr

def satisfy_conditions(idx_sg: list, c: int, descr: list, cq_satisfied: list):
    
    return sufficient_subgroup_size(idx_sg, c) and not(similar_description(descr, cq_satisfied))
