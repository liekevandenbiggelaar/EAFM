from datetime import datetime, timedelta
import numpy as np
import heartpy as hp


def weighted_moving_average(ecg, sigma = 2, M = 10):
    
    weights = np.exp(-(np.arange(M) - (M - 1) / 2 )**2 / (2 * sigma **2))
    weights /= np.sum(weights)
    
    return np.convolve(ecg, weights, mode='valid')

def ecg_invert(ecg: list):

    # Check if the signal is inverted
    ecg_meanzero = ecg - np.nanmean(ecg)
    window_shape = min(len(ecg_meanzero), 2000)
    x_rolled = np.lib.stride_tricks.sliding_window_view(ecg_meanzero, window_shape, axis=0)
    
    shape = np.array(x_rolled.shape)
    shape[-1] = -1
    max_squared = np.take_along_axis(x_rolled, np.square(x_rolled).argmax(-1).reshape(shape), axis=-1)
    med_max_squared = np.nanmedian(max_squared)
    
    # If it is inverted, change back
    if med_max_squared < 0:
        was_inverted = True
        ecg = np.array(ecg) * -1 + 2 * np.nanmean(ecg)
    else:
        was_inverted = False

    return ecg, was_inverted
                                   