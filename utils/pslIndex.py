import sys
sys.path.append('../')
import utils._indexDefinitions as _index
import utils.climatology as climat

import cftime
import xarray
import re

def calculateClimatology(climatDs, *args):
    
    """From a provided dataset, start year and finish year, return the calculated mean for every psl lat defined in _indexDefinitions file.
    
    
    Useage
    calculateClimatology(climatDs) #calculates for all years
    
    Or to use a subset of the years
    calculateClimatology(climatDs, climatStart, climatFinish)
    
    """
    
    
    
    #check the input is actually an xarray
    regex=re.compile('xarray')
    if regex.search(str(climatDs))==None:
        raise(EnvironmentError("Climatology Ds provided is not an xarray"))

    #tidy up input data so the variable names are common between CMIP and CESM
    if any([hasattr(climatDs, 'project_id'), hasattr(climatDs, 'mip_era')]):
        if climatDs.mip_era=='CMIP6':
            climatDs=climatDs.rename_vars({'psl':'PSL'})

    #output Ds
    climatologyDs=xarray.Dataset(coords={"time":climatDs.time})
    
    #The two latitudes of interest are defined in _indexDefinitions
    domain = _index.pslIndex['sam']
    
    #for each latitude, calculate the climatology 
    for keys in domain:
        
        domainDs=climatDs.PSL.sel(lat=domain[keys],method='nearest', drop=True)
        
        if len(args)==2:
            #reduce domain by years provided
            domainDs=climat.dateInterval(domainDs, args[0], args[1])
        elif len(args)!=0:
            raise(Error("Wrong number of inputs provided"))
        
        climatologyDs[keys]=domainDs.mean(dim='lon')
    
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
 

    #tidy up input data so the variable names are common between CMIP and CESM
    if any([hasattr(ds, 'project_id'), hasattr(ds, 'mip_era')]):
        if ds.mip_era=='CMIP6':
            ds=ds.rename_vars({'psl':'PSL'})
    else:
        print('Ds looks like CESM') #CESM-LME
    
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
