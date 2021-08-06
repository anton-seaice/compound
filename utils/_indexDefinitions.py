
# This dict is a container for the areas to calculate SST anomalies for when calculting SST indeces

sstIndex = {
    #"nino12" : {"latMin":-10, "latMax":0, "longMin":270,"longMax":280} ,
    #"nino3" : {"latMin":-5, "latMax":5, "longMin":210,"longMax":270},
    "nino34" : {"latMin":-5, "latMax":5, "longMin":190,"longMax":240},
    "nino4" : {"latMin":-5, "latMax":5, "longMin":160,"longMax":210},
    "westIO" : {"latMin":-10, "latMax":10, "longMin":50,"longMax":70},
    "eastIO" : {"latMin":-10, "latMax":0, "longMin":90,"longMax":110},  # This is the 'traditional/Saji area'
    "backgroundSst" : {"latMin":-20, "latMax":20, "longMin":0,"longMax":360} # use to detrend indeces
} 

# This is the latitudes to use for sam calculations
pslIndex = {
    "sam" : {"lat1":-40, "lat2":-65} 
}

# This is the months of interest for each index when calculating warm-season averages
monthsOfInterest = {
    "nino3" :[7,15] ,
    "nino34NoDetrend" : [7,15] ,
    "nino4NoDetrend" : [7,15] ,
    "eastIONoDetrend" : [7,12] , 
    "dmi": [7,12] ,
    "nino34" : [7,15] ,
    "nino4" : [7,15] ,
    "eastIO" : [7,12] , 
    "sam" : [10, 15] ,
    "lat1" : [10, 15],
    "lat2" : [10, 15],
    "precAnom" : [10, 15] ,
    "tsAnom" : [10, 15], 
    "pr" : [10, 15] ,
    "tas" : [10, 15], 
    "enso" : [12,14], 
    "eIndex" :  [7,15] ,
    "cIndex" :  [7,15] ,
    "backgroundSstNoDetrend" : [7,15]
}

nDaysOfInterest = {
    "precAnom" : (30+31+30+31+31+28+31) # Sept (month 9) to March (month 15), No Leap
}

# This is the list of indices which are fire promoting when positive in the warm-season
firePos = ['nino34', 'nino4', 'dmi', 'nino34NoDetrend', 'nino4NoDetrend', 'eIndex','cIndex','NCT', 'NWP']

# This is indices which are fire promiting when negative in the warm-seaonon
fireNeg = ['sam', 'eastIO','samMarshall', 'samFogt']

# List of indices we could use for ENSO
enso = ['nino3', 'nino34', 'nino4', 'nino3NoDetrend', 'nino34NoDetrend', 'nino4NoDetrend', 'ecCombined', 'eIndex', 'cIndex', 'NCT', 'NWP']

# Indices we might use for IOD
iod = ['dmi', 'eastIO', 'eastIONoDetrend']

# Indices we might use for SAM
sam = ['sam', 'samMarshall', 'samFogt']