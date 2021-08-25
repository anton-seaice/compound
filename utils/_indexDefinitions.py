
# This dict is a container for the areas to calculate SST anomalies for when calculting SST indeces
sstIndex = {
    "nino1+2" : {"latMin":-10, "latMax":0, "longMin":270,"longMax":280} ,
    "nino3" : {"latMin":-5, "latMax":5, "longMin":210,"longMax":270},
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

# This is the months of interest for each index when calculating seasonal averages
monthsOfInterest = {
    "nino3" :[7,15] ,
    "nino34NoDetrend" : [7,15] ,
    "nino4NoDetrend" : [7,15] ,
    "westIONoDetrend" : [7,12] , 
    "eastIONoDetrend" : [7,12] , 
    "dmi": [7,12] ,
    "nino34" : [7,15] ,
    "nino4" : [7,15] ,
    "eastIO" : [7,12] , 
    "westIO" : [7,12] , 
    "samSummer" : [10,15] ,
    "samWinter" : [4,9] ,
    "pr" : {'winter':[4,9],'summer':[10,15]} ,
    "ts" : {'winter':[4,9],'summer':[10,15]} ,
    "eIndex" :  [7,15] ,
    "cIndex" :  [7,15] ,
    "backgroundSstNoDetrend" : [7,15]
}

# This is the list of indices which are fire promoting when positive when calculating events
firePos = [
    'nino34', 'nino4', 'eIndex','cIndex','NCT', 'NWP',
    'dmi',
    'samWinter'
]

# This is indices which are fire promiting when negative in the warm-season when calculating events
fireNeg = ['samSummer', 'eastIO']

#When calculating compounds, one index each for enso+iod+sam is required
# List of indices we could use for ENSO
enso = [
    'nino3', 'nino34', 'nino4',
    'ecCombined', 'eIndex', 'cIndex', 
    'NCT', 'NWP'
]

# Indices we might use for IOD
iod = ['dmi', 'eastIO']

# Indices we might use for SAM
sam = ['samSummer', 'samWinter']