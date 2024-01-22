import numpy as np
import lightkurve as lk
import os
import pywt
from bisect import bisect_left
from astropy.timeseries import LombScargle

def get_all_files(folder_path):
    file_paths = []  # List to store file paths
    # Traverse through the folder and its subfolders
    for root, directories, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)  # Create the file path
            file_paths.append(file_path)  # Append the file path to the list

    return file_paths

def CleanLC(LC, SaveName="Default", DiagnosticPlot=False):
    '''
    Takes in the Lightkurve lightcurve class and returns array of time and flux after cleaning.
    '''
    #Time = LC.time.jd
    #Flux = LC.flux.value
    Time = np.array(LC.time.jd)
    Flux = np.array(LC.flux.value)
    
    #Try to get the quality flux, and marked as an outlier
    try:
        Quality = LC.quality.value == 0
    except:
        Quality = np.ones(len(Time)).astype(np.bool_) 
   
    #Remove NanFlux
    NanFlux = np.logical_or(np.logical_or(np.isnan(Time), np.isnan(Flux)), ~Quality)
    Time = Time[~NanFlux]
    Flux = Flux[~NanFlux]   
    Flux /= np.median(Flux)


    return Time, Flux

 

def Spectrogram(Time, Flux, NPERSEG=1024):
    deltaT = np.median(np.diff(Time))
    fs = 1/np.median(deltaT)
   
    #frequencies_ls = np.linspace(0.1, fs/2, (nperseg+1)*2)  # Frequency range to compute periodogram
    spectrogram_ls = []

    start = 0
    overlap = 0.5  # Overlap between segments

    print("Instead of indexing use time to define the chunk")
    
    Tolerance = deltaT/20.
    start = np.min(Time)-Tolerance
    LengthTime = len(Time)

    print("The shape of time is given by:", np.shape(Time))


    Interval = NPERSEG*deltaT
    frequencies_ls = np.linspace(1./Interval, fs/2, NPERSEG*30)  # Frequency range to compute periodogram
    while 1:
        StartIndex = bisect_left(Time, start)
        StopIndex = bisect_left(Time, start+Interval+2*Tolerance)
        if StartIndex+1>LengthTime:
            break
        TimeSegment = Time[StartIndex:StopIndex]
        FluxSegment = Flux[StartIndex:StopIndex]
        if len(TimeSegment)<10:
            periodogram_ls = np.zeros(len(frequencies_ls))
        else:
            periodogram_ls = LombScargle(TimeSegment, FluxSegment,normalization='psd').power(frequencies_ls)
        spectrogram_ls.append(periodogram_ls)
        start += Interval

    spectrogram_ls = np.array(spectrogram_ls).T  # Transpose for plotting
    LenFs, LenT  = np.shape(spectrogram_ls)
    T = np.linspace(min(Time), max(Time), LenT)
    return frequencies_ls, T, spectrogram_ls


