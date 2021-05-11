import sys
sys.path.append('../')
import utils._indexDefinitions as _index
import utils.climatology as climat

import cftime
import xarray
import re

def calculateClimatology(climatDs, climatStart, climatFinish):
    
    #check the input is actually an xarray
    regex=re.compile('xarray')
    if regex.search(str(climatDs))==None:
        raise(EnvironmentError("Climatology Ds provided is not an xarray"))

    #some output Ds
    domainDs=xarray.Dataset(coords={"time":climatDs.time})
    climatologyDs=domainDs.copy()
    
    #The two latitudes of interest are defined in _indexDefinitions
    domain = _index.pslIndex['sam']
    
    #for each latitude, calculate the climatology 
    for keys in domain:
        climatologyDs[keys]=climat.dateInterval(
            climatDs.sel(lat=domain[keys],method='nearest', drop=True).PSL.mean(dim='lon'),
            climatStart,
            climatFinish
        )
        
    return climatologyDs
        
        
def calculateSamIndex(ds, *args):
    
    """
    This function calculates sam index based on monthly climatology.
    
    inputs:
    
    xarray ds in CESM format
    start and finish years to use for climatology (e.g. calculateSamIndex(ds, startYear, finishYear))
    or climatologyDs (e.g. calculateSamIndex(ds, climatologyDs))
    
    
    output:
    
    new xarray with time dimension
        
    """
    
    if len(args)==1:
            #check the argument is actually an xarray
            regex=re.compile('xarray')
            if regex.search(str(type(args[0])))!=None:
                #use this argument for climatology instead
                climatologyDs=args[0]
            else:
                raise(EnvironmentError("Climatology Ds provided is not an xarray"))
    elif len(args)!=2:
        raise(EnvironmentError("Too many input arguments provided"))
    
    #The two latitudes of interest are defined in _indexDefinitions
    domain = _index.pslIndex['sam']
    
    #ds for output
    samIndex=xarray.Dataset(coords={"time":ds.time})
    
    domainDs=samIndex.copy()
    normalisedDs=samIndex.copy()
    
    #for each latitude, calculate the climatology and normalise
    for keys in domain:
        #this is the data we want to calculate the index using
        domainDs[keys]=ds.sel(lat=domain[keys],method='nearest', drop=True).PSL.mean(dim='lon')
        
        #if there were two arguments given for climatology, use the same data
        if len(args)==2:
            try:
                climatologyDs[keys]=climat.dateInterval(domainDs[keys], int(args[0]), int(args[1]))
            except:
                #There is an assumption here the error is that in couldn't cast the inputs to int
                raise(EnvironmentError("Input Year Range not recognised"))
                
        #normalise 
        normalisedDs[keys]=climat.normalise(domainDs[keys],climatologyDs[keys])

    samIndex['sam']=normalisedDs['lat1']-normalisedDs['lat2']
    
    return samIndex


"""
    #average across each latitude of interest
    ds40=ds.sel(lat=domain['lat1'],method='nearest', drop=True).PSL.mean(dim='lon')
    ds65=ds.sel(lat=domain['lat2'],method='nearest', drop=True).PSL.mean(dim='lon')
    
    if len(args)==0:
        #filter by the climatology
        ds40Climatology = climat.dateInterval(ds40, climatStart, climatFinish)
        #filter by the climatology
        ds65Climatology = climat.dateInterval(ds65, climatStart, climatFinish)
    elif len(args)==1:
        regex=re.compile('xarray')
        if regex.search(str(type(args[0])))!=None:
            climatDs=args[0]
            
            climatDs40=climatDs.sel(lat=domain['lat1'],method='nearest', drop=True).PSL.mean(dim='lon')
            climatDs65=climatDs.sel(lat=domain['lat2'],method='nearest', drop=True).PSL.mean(dim='lon')
            
            ds40Climatology = climat.dateInterval(climatDs40, climatStart, climatFinish)
            ds65Climatology = climat.dateInterval(climatDs65, climatStart, climatFinish)
    else:
        raise(EnvironmentError("Climatology Ds provided is not an xarray"))
    """
    