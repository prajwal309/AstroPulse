import numpy as np
import lightkurve as lk
import os

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