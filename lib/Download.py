
import pandas as pd
import lightkurve as lk
import os

def downloadLightcurve(KIC):
    TargetName = "KIC"+str(KIC) 

    LCSaveDirectory = 'lc_data/'+TargetName
    if not(os.path.exists(LCSaveDirectory)):
        os.mkdir('lc_data/'+TargetName)

    Kepler_Files = lk.search_lightcurve(TargetName, mission="Kepler")
   
   
    #This are for Kepler data    
    for i in range(len(Kepler_Files)):
        try:
            Kepler_Files[i].download(download_dir='lc_data/'+TargetName)    
        except:
            print("No Kepler data found.")
        

