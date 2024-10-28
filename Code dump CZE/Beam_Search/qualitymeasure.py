import numpy as np
import pandas as pd
import math

def compute_qualitymeasure(theta_1: float, theta_2: float, idx_sg: list, idx_compl: list):
    ef = entropy_function(idx_sg, idx_compl)
    return round(ef * ( theta_1 - theta_2 ), 2 ) #verm met entropy functie

def entropy_function(idx_sg: list, idx_compl: list):
    n = len(idx_sg)
    nC = len(idx_compl)
    N = n + nC
    
    if n == 0 or nC == 0:
        return 0
    
    p_e = n / N
    p_f = nC / N
    
    ef = -p_e * math.log(p_e) + p_f * math.log(p_f)
    
    return ef


def compute_theta(target_data=None, theta='RMSSD', subgroup=None):
    
    if len(subgroup) == 26:
        val = np.mean(np.array(target_data[theta]))
    else:
        pids = list(subgroup['PID'])
        selection = target_data[target_data['PID'].isin(pids)]
        val = np.mean(np.array(selection[theta]))

    return val
    
##### HEART RATE VARIABILITY #####
def RMSSD(deltaRR: list):
    """ Computing the root mean square of successive RR interval differences. """

    sq_deltaRR = np.square(deltaRR)
    sum_deltaRR = np.sum(sq_deltaRR)
    RMSSD = np.sqrt( 1/(len(deltaRR) - 1) * sum_deltaRR)
    
    return round(RMSSD, 2)


def SDSD(deltaRR: list):
    """ Computing the standard deviation of diﬀerences between adjacent RR intervals. """
    
    mean_deltaRR = np.mean(deltaRR)
    diff_deltaRR = np.array([ i - mean_deltaRR for i in deltaRR ])
    sq_deltaRR = np.square(diff_deltaRR)
    sum_deltaRR = np.sum(sq_deltaRR)
    SDSD = np.sqrt( 1/(len(deltaRR) - 2) * sum_deltaRR)
    
    return round(SDSD, 2)

def SDRR(RR: list):
    """ Computing the standard deviation of diﬀerences between adjacent RR intervals. """

    mean_RR = np.mean(RR)
    diff_RR = np.array([ i - mean_RR for i in RR ])
    sq_RR = np.square(diff_RR)
    sum_RR = np.sum(sq_RR)
    SDRR = np.sqrt( 1/(len(RR) - 1) * sum_RR)
    
    return round(SDRR, 2)
    
    
##### P-WAVE EXISTENCE #####
def P_count(P_binary: list):
    return np.sum(np.array(P_binary))/len(P_binary)*100

def F_count(F_binary: list):
    return np.sum(np.array(F_binary))/len(F_binary)*100

def extra_wave_count(extra_waves: list):
    return np.sum(np.array(extra_waves)/len(extra_waves)*100)


#### Combination of HRV and P ####
def SDSD_P(deltaSQ: list, P_binary: list):
    
    deltaSQ_P = [deltaSQ[i] * P_binary[i] for i in range(len(deltaSQ))]
    
    mean_deltaSQ = np.mean(deltaSQ)
    diff_deltaSQ = np.array([ i - mean_deltaSQ for i in deltaSQ_P ])
    sq_deltaSQ = np.square(diff_deltaSQ)
    sum_deltaSQ = np.sum(sq_deltaSQ)
    SDSD_P = np.sqrt( 1/(len(deltaSQ_P) - 2) * sum_deltaSQ)
    
    return round(SDSD_P, 2)

def SDSD_F(deltaSQ: list, F_binary: list):
    
    deltaSQ_F = [deltaSQ[i] * F_binary[i] for i in range(len(deltaSQ))]
    
    mean_deltaSQ = np.mean(deltaSQ)
    diff_deltaSQ = np.array([ i - mean_deltaSQ for i in deltaSQ_F ])
    sq_deltaSQ = np.square(diff_deltaSQ)
    sum_deltaSQ = np.sum(sq_deltaSQ)
    SDSD_F = np.sqrt( 1/(len(deltaSQ_F) - 2) * sum_deltaSQ)
    
    return round(SDSD_F, 2)

def SDRR_P(SQ: list, P_binary: list):
    
    SQ_P = [SQ[i] * P_binary[i] for i in range(len(SQ))]
    
    mean_SQ = np.mean(SQ)
    diff_SQ = np.array([ i - mean_SQ for i in SQ_P ])
    sq_SQ = np.square(diff_SQ)
    sum_SQ = np.sum(sq_SQ)
    SDRR_P = np.sqrt( 1/(len(SQ_P) - 1) * sum_SQ)
    
    return round(SDRR_P, 2)

def SDRR_F(SQ: list, F_binary: list):
    
    SQ_F = [SQ[i] * F_binary[i] for i in range(len(SQ))]
    
    mean_SQ = np.mean(SQ)
    diff_SQ = np.array([ i - mean_SQ for i in SQ_F ])
    sq_SQ = np.square(diff_SQ)
    sum_SQ = np.sum(sq_SQ)
    SDRR_F = np.sqrt( 1/(len(SQ_F) - 1) * sum_SQ)
    
    return round(SDRR_F, 2)

def RMSSD_P(deltaSQ: list, P_binary: list):

    deltaSQ_P = [deltaSQ[i] * P_binary[i] for i in range(len(deltaSQ))]
    
    sq_deltaSQ = np.square(deltaSQ)
    sum_deltaSQ = np.sum(sq_deltaSQ)
    RMSSD_P = np.sqrt( 1/(len(deltaSQ_P) - 1) * sum_deltaSQ)
    
    return round(RMSSD_P, 2)

def RMSSD_F(deltaSQ: list, F_binary: list):

    deltaSQ_F = [deltaSQ[i] * F_binary[i] for i in range(len(deltaSQ))]
    
    sq_deltaSQ = np.square(deltaSQ)
    sum_deltaSQ = np.sum(sq_deltaSQ)
    RMSSD_F = np.sqrt( 1/(len(deltaSQ_F) - 1) * sum_deltaSQ)
    
    return round(RMSSD_F, 2)

