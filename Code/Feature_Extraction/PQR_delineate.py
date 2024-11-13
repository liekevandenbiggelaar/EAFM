import heartpy as hp
import neurokit2 as nk
import matplotlib.pyplot as plt
import numpy as np
import scipy
import ast

from Code.Preprocessing.cleaning import weighted_moving_average, ecg_invert
from Code.Analysis.visualizations import create_avg_plot


# ========= R-PEAK DETECTION: DONE =========== #

def R_peak_detection(ecg: list, rate: int):
    """ 
    Locate R-peaks in a signal. 

    PARAMS
    * ecg: list(int) - A list with the (filtered) values of the ECG.
    
    RETURNS
    * R: list(int) - A list with the index that represents the place of the R-peaks.
    """

    _, results = nk.ecg_peaks(ecg, sampling_rate=rate)
    R = results['ECG_R_Peaks']
        
    return R 


def R_peak_interval(R, rate: int):
    RR = []
    R_correct = []
    maxdiff = round(rate / 2, 0)

    while len(R) != 0:
        if len(R) != 1:
            R0, R1 = R[0: 2]
            diff = R1 - R0
            
            if diff < maxdiff and len(R) != 2: # Correction for faulty R peaks
                R2 = R[2]
                nextdiff = R2 - R1
                if len(RR) != 0:
                    lastdiff = RR[-1]
                    
                    if nextdiff >= lastdiff:
                        R.pop(0)
                    elif lastdiff > nextdiff:
                        R.pop(1)
                else:
                    R.pop(1)
            else:
                R.pop(0)
                R_correct.append(R0)
                if diff < 1000: # meer dan dit kan niet goed zijn
                    RR.append(diff)
                else: 
                    continue
            
        else:
            R_correct.append(R[0])
            R.pop(0)
        
        
        
    return RR, R_correct

def RR_interval_difference(RR):
    return list(np.abs(np.diff(np.array(RR))))
            


# ========= QRS-COMPLEX DETECTION: DONE =========== #
def QRS_delineate(ecg, R, rate=500):
    
    waves, _ = nk.ecg_delineate(ecg, rpeaks=R, sampling_rate=rate)
    
    return waves

def Q_S_peak_detection(waves: dict):
    """ 
    Locate Q- and S-peaks (local minima) in a signal within second half of the RR-intervals. 
    """
        
    Q = [ i for i in range(len(waves['ECG_Q_Peaks'])) if waves['ECG_Q_Peaks'][i] == 1 ]
    S = [ j for j in range(len(waves['ECG_S_Peaks'])) if waves['ECG_S_Peaks'][j] == 1 ]
    
    return Q, S


def QRS_duration(Q: list, S: list, avg_RR: int):

    # Find a good S peak for each Q peak
    max_duration = avg_RR 
    QS = []
    
    # Go over all Q-peaks
    while len(Q) != 0 and len(S) != 0:
        Q_i = Q[0]
        S_i = S[0]
        duration = S_i - Q_i
        
        # Check if there is a S- for the Q-peak
        if duration > max_duration:
            Q.pop(0)
        
        # Check if there is a Q- for the S-peak
        elif duration < 0:
            S.pop(0)
        
        # Otherwise it is a match!
        else:
            QS.append( duration )
            Q.pop(0)
            S.pop(0)
            
    return QS
                                  
# ======= WAVE DETECTION ALGORITHMS ======= #                                  
def wave_detection(ecg: list, S: list, Q: list, wid: str, first_wid: int, avg_PQ=None, avg_count=None):
    """ 
    
    Locate P, T (or F) waves in a signal within the SQ-interval using local maxima. 
    
    PARAMS
    ========
    * ecg: list(int) - A list with the (filtered) values of the ECG.
    * S: list(int) - A list with the indices of the identified S-peaks.
    * Q: list(int) - A list with the indices of the identified Q-peaks.
    
    RETURNS
    ========
    * waves: list(int) - A list with the index that represents the peaks of all waves within the RQ-interval.
    
    """
    waves_indices = []
    waves_count = []
    Q_peaks_correct = []
    PQs = []
    SQ = []
    
    while len(S) != 0 and len(Q) != 0:
        S_i = S[0]
        Q_i = Q[0]
        
        if len(S) > 1:
            if S[1] < Q_i:
                S.pop(0)
            elif Q_i < S_i:
                Q.pop(0)
            elif Q_i == S_i:
                S.pop(0)
                Q.pop(0)
            else:
                segment = ecg[S_i: Q_i]

                segment = weighted_moving_average(segment, sigma=20, M=10)
                #segment = weighted_moving_average(segment, sigma=25, M=50)
                segment = np.array(scale_segment(segment))
                

                peaks, _ = scipy.signal.find_peaks(segment)
                
                peaks = [p for p in peaks if segment[p] > 0.1]
                
                # Count Waves
                nr_peaks = len(peaks)
                
                # P-Wave Existence Preparation
                peaks = [ x + S_i + 3 for x in peaks ]
                SQ_i = Q_i - S_i
                SQ.append(SQ_i)
                
                Q_peaks_correct.append(Q_i)
                if wid == str(first_wid) and Q_i <= ((20*60*1000)/2) and len(peaks) != 0:
                    PQ_interval = Q_i - peaks[-1]
                    PQs.append(PQ_interval)
                
                # Continue to next SQ-interval
                S.pop(0)
                Q.pop(0)
            
                waves_indices = waves_indices + peaks
                waves_count.append(nr_peaks)
        else:
            S = []
            Q = []
    
    # Find averages
    if wid == str(first_wid):
        avg_count, diff_waves = extra_waves(waves_count, wid, str(first_wid), t=20)
        avg_PQ = np.mean(np.array(PQs))
    else:
        avg_waves, diff_waves = extra_waves(waves_count, wid, str(first_wid), avg=avg_count, t=20)
        avg_PQ = avg_PQ
            
    return waves_count, diff_waves, waves_indices, Q_peaks_correct, SQ, avg_PQ, avg_count


def P_existence(waves: list, Q: list, avg_PQ: int, t=20):
    """  """
    
    P_binary = []
    F_binary = []
    Q_prev = 0
    
    # go over all Q-peaks
    for i in range(len(Q)):
        Q_i = Q[i]
        
        compl_waves = [w for w in waves if Q_prev <= w <= Q_i]
        limit = Q_i - round( 1.2 * avg_PQ )  
        PQ_max = [r for r in compl_waves if limit <= r ]
        
        if len(PQ_max) == 0:
            P_binary.append(1) # No Existing P-wave (situation (c))
            F_binary.append(0)
        
        elif len(PQ_max) > 3:
            P_binary.append(1) # F-waves! (situation (b))
            F_binary.append(1)
        
        else:
            P_binary.append(0) # Existing P-wave, no F-waves (situation (a))
            F_binary.append(0)
    
    return P_binary, F_binary


def scale_segment(x: list):
    
    max_seg = max(x)
    min_seg = min(x)
    
    z = [ (x_i - min_seg)/(max_seg - min_seg) for x_i in x ]
    
    return z


def extra_waves(wave_count: list, wid, first_wid, avg=None, t=20):
    """ Using the average of the first t(=20) minutes. 
        Use average of the first 20 mins of the first wave. """
    
    if wid == str(first_wid):
        limit = round( ( t * 60 * 1000 ) / 2 )
        avg_waves = round( np.mean( np.array(wave_count[:limit])) )
        extra_waves = [ w - avg_waves for w in wave_count ]
    else:
        avg_waves = avg
        extra_waves = [ w - avg_waves for w in wave_count ]
    
    return avg_waves, extra_waves


def SQ_interval_difference(SQ):
    return list(np.abs(np.diff(np.array(SQ))))


##################### DELINEATE ALL ############################
                                  
def extract_features(ecg: list, pid: str, wid: str, avg_PQ, avg_count, rate=500):
    
    features = {}
    
    features['PID'] = [pid]
    features['WID'] = [wid]
    
    #plt.scatter(R, ecg[R], color='orange')
    ecg, inverted = ecg_invert(ecg)
    ecg = hp.filter_signal(ecg, cutoff = 0.75, sample_rate = rate, filtertype='highpass')
    ecg = weighted_moving_average(ecg, sigma=20, M=10)
    
    
    # R-peak 
    try:
        R = R_peak_detection(ecg, rate)
        
    except:
        return features, avg_PQ, avg_count

    if len(R) <= 1:
        return features, avg_PQ, avg_count
    
    RR, R = R_peak_interval(list(R), rate) 
    deltaRR = RR_interval_difference(RR)
    # avg = create_avg_plot(ecg, R)
    
    features['R-location'] = [int(i) for i in R]
    features['RR-interval'] = [int(j) for j in RR]
    features['RR-difference'] = [int(m) for m in deltaRR]
    

    # QRS-complex
    try:
        waves = QRS_delineate(ecg, R, rate)
        Q, S = Q_S_peak_detection(waves)
        
    except:
        Q, S, = [], []
    
    features['Q-location'] = [Q]
    features['S-location'] = [S]
    
    
    # Wave Detection
    if len(RR) == 0:
        avg_RR = 0
    else:
        avg_RR = np.mean(np.array(RR))
        
    if len(Q) != 0 and len(S) != 0:
        QRS = QRS_duration(Q.copy(), S.copy(), avg_RR)
        
        waves_count, extra_waves, wave_indices, Q_peaks_correct, SQ, avg_PQ, avg_count = wave_detection(ecg, S.copy(), Q.copy(), wid, '1', avg_PQ, avg_count)
        P_binary, F_binary = P_existence(wave_indices, Q_peaks_correct, avg_PQ)
        delta_SQ = SQ_interval_difference(SQ)
    else:
        QRS, wave_indices, waves_count = [], [], []
    
    # plt.figure(figsize=(15,10))
    # plt.plot(range(len(ecg)), ecg)
    # plt.scatter(R, ecg[R], color='orange')
    # plt.scatter(Q, ecg[Q], color='red')
    # plt.scatter(S, ecg[S], color='green')
    # plt.scatter(wave_indices, ecg[wave_indices], color='grey')
    # plt.show()
    
    features['QRS-duration'] = [QRS]
    features['SQ-duration'] = [SQ]
    features['SQ-difference'] = [int(c) for c in delta_SQ]
    
    features['Wave Count'] = [waves_count]
    features['Extra Waves'] = [extra_waves]
    features['P-existence'] = [P_binary]
    features['F-existence'] = [F_binary]
    
    return features, avg_PQ, avg_count
