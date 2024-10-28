import matplotlib.pyplot as plt
import numpy as np

def preprocessing_waveform(df, df_wf, label:int, index=0, low=0.75, high=6.5):
    """ 
    
    The processes of translating and cleaning a waveform.
    
    PARAMS
    ========
    * df: pd.DataFrame - The dataframe with the wavesamples for that patient.
    * label: int - an integer that represents the label that you want, this is different for each patient.
    * index: int (default 0) - which of the recording periods do you want to analyse? 
    * df_wf: pd.DataFrame (default df_wf) - The dataframe that represents the measuring instruments.
    * low: int (default 0.75) - The cut-off of the low frequency of the noise.
    * high: int (default 6.5) - The cut-off of the high frequency of the noise.
    
    RETURNS
    ========
    * clean_wave_sample: list(int) - A list with the cleaned waveform values.
    
    """

    wave_sample = df.iloc[label]['WaveSamples'][index]
    pid = df.iloc[label]['PatientID']
    label = df.iloc[label]['Label']
    
    translated_wave_sample = translate_WaveSample(wave_sample, pid, label, df_wf)
    clean_wave_sample = denoise(translated_wave_sample, low, high)
    
    return clean_wave_sample


def create_avg_plot(values, peaks):
    """
    Show the ECG waveforms of one patient in an interactive plot, 
    with the option to determine how many heartbeats you want to show.
        
    PARAMS
    values: segment of the ECG.
    peaks: the location of the R-peaks in the segment.
    """
        
    vals = values
    plt.figure(figsize=(8,10))

    # Create a list of heart beats
    Rpeaks = np.array(peaks)
    rr_intervals = np.diff(Rpeaks)

    heartbeats = []
    startpeak = Rpeaks[0]
    for i in range(len(Rpeaks)):
        if (i == 0):
            continue
        rate = rr_intervals[i-1]
        half_rate = round(rate / 2)
        prev_peak = Rpeaks[i - 1]
        current_peak = Rpeaks[i]

        prev_start = int(prev_peak - half_rate)
        current_start = int(current_peak - half_rate)

        hb = vals[prev_start: current_start]
        heartbeats.append( hb )
    
    for beat in heartbeats:
        plt.plot(beat, color='gray', alpha=0.05)
        
    # Create the averages
    # Determine the average length of the lists
    avg_length = round(np.mean([len(beat) for beat in heartbeats]))
        
    # Rescale the lists to have the same length by interpolating values
    rescaled_lists = [np.interp(np.linspace(0, 1, avg_length), np.linspace(0, 1, len(beat)), beat) for beat in heartbeats if len(beat) > 0]

    # Calculate the average of the rescaled lists
    average = np.mean(rescaled_lists, axis=0)
    times = [ i * 0.002 for i in range(len(average))]
    plt.plot(list(average), color='orange')
    plt.ylim(-0.3, 0.3)
    plt.xlim(0, avg_length)
    plt.xlabel("Duration (2 ms)")
    plt.ylabel("Amplitude (mV)")
    plt.grid(True)
    plt.title('Average heartbeat recorded from lead II for one patient')
    plt.show()
    
    return average


def plot_differences(original, denoised):
    
    plt.figure(figsize=(24,8))
    plt.plot(denoised, label='Denoised signal')
    plt.plot(original, label='Original signal')
    plt.grid()
    plt.xlabel('Time (ms)')
    plt.ylabel('Amplitude (V)')
    plt.title('The signal before and after denoising techniques')
    plt.legend()
    plt.xlim(0, max(len(original), len(denoised)))
    plt.show()