import pandas as pd
import ast

import Code.Beam_Search.qualitymeasure as qm

def compute_qualitymeasures(path: str, savepath: str):
    
    metadata = pd.read_csv(path)
    
    sdsd_all, rmssd_all, sdrr_all = [], [], []
    pcount_all, fcount_all, wavescount_all = [], [], []
    sdsd_pall, sdrr_pall, rmssd_pall = [], [], []
    sdsd_fall, sdrr_fall, rmssd_fall = [], [], []
    
    for i in range(len(metadata)):
        RR = ast.literal_eval(metadata.iloc[i]['RR-interval'])
        deltaRR = ast.literal_eval(metadata.iloc[i]['RR-difference'])
        P_binary = ast.literal_eval(metadata.iloc[i]['P-existence'])
        F_binary = ast.literal_eval(metadata.iloc[i]['F-existence'])
        extra_waves = ast.literal_eval(metadata.iloc[i]['Extra Waves'])
        SQ = ast.literal_eval(metadata.iloc[i]['SQ-duration'])
        deltaSQ = ast.literal_eval(metadata.iloc[i]['SQ-difference'])
        
        sdsd = qm.SDSD(deltaRR)
        rmssd = qm.RMSSD(deltaRR)
        sdrr = qm.SDRR(RR)
        
        pcount = qm.P_count(P_binary)
        fcount = qm.F_count(F_binary)
        wavescount = qm.extra_wave_count(extra_waves)
        
        sdsd_p = qm.SDSD_P(deltaSQ, P_binary)
        sdsd_f = qm.SDSD_F(deltaSQ, F_binary)
        sdrr_p = qm.SDRR_P(SQ, P_binary)
        sdrr_f = qm.SDRR_F(SQ, F_binary)
        rmssd_p = qm.RMSSD_P(deltaSQ, P_binary)
        rmssd_f = qm.RMSSD_F(deltaSQ, F_binary)
        
        sdsd_all.append(sdsd)
        rmssd_all.append(rmssd)
        sdrr_all.append(sdrr)
        
        pcount_all.append(pcount)
        fcount_all.append(fcount)
        wavescount_all.append(wavescount)
        
        sdsd_pall.append(sdsd_p)
        sdsd_fall.append(sdsd_f)
        sdrr_pall.append(sdrr_p)
        sdrr_fall.append(sdrr_f)
        rmssd_pall.append(rmssd_p)
        rmssd_fall.append(rmssd_f)
        
        
    quality_table = pd.DataFrame()
    quality_table['PID'] = metadata['PID']
    quality_table['SDSD'] = sdsd_all
    quality_table['RMSSD'] = rmssd_all
    quality_table['SDRR'] = sdrr_all
    
    quality_table['P-count'] = pcount_all
    quality_table['F-count'] = fcount_all
    quality_table['Extra-Average'] = wavescount_all
    
    quality_table['SDSD_P'] = sdsd_pall
    quality_table['RMSSD_P'] = rmssd_pall
    quality_table['SDRR_P'] = sdrr_pall
    
    quality_table['SDSD_F'] = sdsd_fall
    quality_table['RMSSD_F'] = rmssd_fall
    quality_table['SDRR_F'] = sdrr_fall
    
    quality_table = quality_table.groupby(['PID'], as_index=False).mean().round(2)
    
    save_path = savepath
    quality_table.to_csv(save_path + "QualityMeasures.csv", index=False)
    
    return quality_table

def remove_qualitymeasures(cols: list):
    metadata = pd.read_csv('/bd-fs-mnt/acacia-working-area/dwc/lieke/MetadataTable.csv')
    
    metadata = metadata.drop(columns=cols)
    
    save_path = '/bd-fs-mnt/acacia-working-area/dwc/lieke/'
    metadata.to_csv(save_path + "MetadataTable.csv", index=False)
    
    return metadata
    