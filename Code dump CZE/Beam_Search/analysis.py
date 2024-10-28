import numpy as np
import pandas as pd

import preprocess as pp
import beam_search as bs

def analysis(data=None, model_params=None, beam_search_params=None, constraints=None, wcs_params=None):

    attributes, descriptives = pp.preprocess()

    beam_search_params['pareto'] = False

    # check if distribution has to be made
    distribution_params = None               

    # a single run
    print(beam_search_params)
    result_emm, general_params, considered_subgroups = bs.beam_search(dataset=data, attributes=attributes, descriptives=descriptives, 
                                                                      model_params=model_params, beam_search_params=beam_search_params, 
                                                                      wcs_params=wcs_params, constraints=constraints)

    result_analysis = result_emm

    return result_analysis, general_params, considered_subgroups, distribution_params
