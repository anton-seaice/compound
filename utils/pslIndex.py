import sys
sys.path.append('../')
import utils._indexDefinitions as _index
import utils.climatology as climat

import cftime
import xarray




def calculateSamIndex(ds, climatStart, climatFinish):
    
    """
    This function calculates sam index based on monthly climatology.
    
    inputs:
    
    xarray ds in CESM format
    start and finish years to use for climatology
    
    output:
    
    new xarray with time dimension
        
    """
    
    #The two latitudes of interest are defined in _indexDefinitions
    domain = _index.pslIndex['sam']
    
    #ds for output
    samIndex=xarray.Dataset(coords={"time":ds.time})

    #average across each latitude of interest
    ds40=ds.sel(lat=domain['lat1'],method='nearest', drop=True).PSL.mean(dim='lon')
    ds65=ds.sel(lat=domain['lat2'],method='nearest', drop=True).PSL.mean(dim='lon')
    
    #filter by the climatology
    ds40Climatology = climat.dateInterval(ds40, climatStart, climatFinish)
    #filter by the climatology
    ds65Climatology = climat.dateInterval(ds65, climatStart, climatFinish)
    
    #normalise each latitude using these climatologies and calculate the difference
    samIndex['sam']=climat.normalise(ds40,ds40Climatology)-climat.normalise(ds65,ds65Climatology)
    
    return samIndex