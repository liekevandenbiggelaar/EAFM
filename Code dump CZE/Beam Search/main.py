import numpy as np
import pandas as pd
import analysis as an

def main(qm=None, beam_search_params=None, model_params=None, date=None,
         constraints=None, wcs_params=None, save_location=None):
    
    data = pd.read_csv("/bd-fs-mnt/acacia-working-area/dwc/lieke/Data2/EPD.csv") #Must still be made!
    
    date = "tbd"
    # location of dfd
    data_output_location = save_location + '/' + str(date) + '_' + str(qm) + '_' + \
        str(list(beam_search_params.values())) + '_' + str(list(constraints.values())) + '_' + \
             + str(list(wcs_params.values())) + '_' + str(list(model_params.values())) + '.xlsx'

    # result_analysis is a df
    print(beam_search_params)
    result_emm, general_params, considered_subgroups, distribution_params = an.analysis(model_params=model_params,
                                                                                        beam_search_params=beam_search_params, 
                                                                                        constraints=constraints,
                                                                                        wcs_params=wcs_params)

    print(result_emm)
    print(general_params)
    print(considered_subgroups)

    # save        
    beam_search_params.update(constraints)
    beam_search_params.update(wcs_params)
    beam_search_params.update(model_params)
    beam_search_params.update({'date': date})
    analysis_info = pd.DataFrame(beam_search_params, index=[0])
    general_params_pd = general_params['params']
    
    dfs = {'result_emm': result_emm, 'analysis_info': analysis_info, 
           'considered_subgroups': pd.DataFrame(considered_subgroups), 
           'general_params_pd': general_params_pd, 
           'distribution_params': pd.DataFrame(distribution_params)}
    
    writer = pd.ExcelWriter(data_output_location, engine='xlsxwriter')
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=True)
    writer.save()    

if __name__ == '__main__':

    # current options for trend_var: prev, prev_slope, mov_prev, mov_prev_slope, mean, ratio
    # current options for hypothesis: data, value
    # current options for value: any value in combination with hypothesis: value
    # current options for use_se (if hypothesis = value): True, False, 'multiply'
    # current options for qm: max, count, average, sum, min
    # current options for threshold: any value (<) in combination with qm: count


    main(data='HBSC_DNSSSU', 
         trend_name='MPALC', 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20}, # 20 descriptive attributes
         model_params = {'trend_var': 'prev', 'hypothesis': 'data', 'value': None, 'use_se': None, 'qm': 'max', 'threshold': None, 'order': 'max'},
         constraints = {'min_size': 0.05, 'min_occassions': 1.0},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, # two times the beam width
         date=20241006, 
         save_location='/bd-fs-mnt/acacia-working-area/dwc/lieke/Data2/EMM_outcomes')
