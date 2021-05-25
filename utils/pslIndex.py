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

    #output Ds
    climatologyDs=xarray.Dataset(coords={"time":climatDs.time})
    
    #The two latitudes of interest are defined in _indexDefinitions
    domain = _index.pslIndex['sam']
    
    #for each latitude, calculate the climatology 
    for keys in domain:
        climatologyDs[keys]=climat.dateInterval(
            climatDs.PSL.sel(lat=domain[keys],method='nearest', drop=True).mean(dim='lon'),
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
    #if there were two arguments given for climatology, use the same data
    elif len(args)==2:
        try:
            climatologyDs=calculateClimatology(ds, int(args[0]), int(args[1]))
        except:
            #There is an assumption here the error is that in couldn't cast the inputs to int
            raise(EnvironmentError("Input Year Range not recognised"))
    else:
        raise(EnvironmentError("Too few/many input arguments provided"))
 
    
    #The two latitudes of interest are defined in _indexDefinitions
    domain = _index.pslIndex['sam']
    
    #grab the data for the two latitues, and name vars 'lat1' and 'lat2'
    domainDs=xarray.merge([
        ds.PSL.sel(
            lat=domain[keys],method='nearest', drop=True
        ).rename(keys).mean(dim='lon') for keys in domain ] 
    )

    #normalise 
    normalisedDs=climat.normalise(domainDs,climatologyDs)
    normalisedDs = normalisedDs.assign_attrs(domain)
    
    #calc
    samIndex=normalisedDs['lat1']-normalisedDs['lat2']
    samIndex=samIndex.rename('sam')
    
    return  samIndex,normalisedDs
