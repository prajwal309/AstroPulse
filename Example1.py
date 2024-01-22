#Created by Prajwal
from lib.Download import downloadLightcurve
from lib.Functions import CleanLC, get_all_files
import numpy as np
import lightkurve as lk
import matplotlib.pyplot as plt


#Read the data 

def RunTarget(Target):

    LightCurvesLocation = "lc_data/KIC"+str(Target) 
   
    

    AllFiles = get_all_files(LightCurvesLocation)
    if len(AllFiles)==0:
        print("Downloading all the Kepler files.")
        downloadLightcurve(Target)
    AllFiles = get_all_files(LightCurvesLocation)    
    print("The length of the all the files are given by ", len(AllFiles))
   
    AllTime = []
    AllFlux = []



    for FileLocation in AllFiles:
       #print("Loading: ", FileLocation) 
       lc = lk.read(FileLocation)
       tess_id = lc.targetid
       Time, Flux  = CleanLC(lc, DiagnosticPlot=False)
       
     
       #Fit a 3 order polynomial
       TrendLine = np.polyval(np.polyfit(Time, Flux, 3), Time)

       #Print Need to find a trendline after masking the transit and occultation
       AllTime.extend(Time)
       AllFlux.extend(Flux)

    if len(AllTime)<10:
        return 0

    AllTime = np.array(AllTime)
    AllFlux = np.array(AllFlux)

    ArrangeIndex = np.argsort(AllTime)

    AllTime = AllTime[ArrangeIndex]-2400000.0
    AllFlux = AllFlux[ArrangeIndex]

    return AllTime, AllFlux

#This is KOI
#RunTarget(8112039)

Time, Flux = RunTarget(2710002)

plt.figure()
plt.plot(Time, Flux, "k.")
plt.xlabel("Time [BJD]")
plt.ylabel("Flux")
plt.tight_layout()
plt.show()