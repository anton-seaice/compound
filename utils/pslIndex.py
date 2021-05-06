import sys
sys.path.append('../')
import utils._indexDefinitions as _index
import utils.climatology as climat

import cftime
import xarray




def calculateSamIndex(ds, climatStart, climatFinish):
    
    domain = _index.pslIndex['sam']
    
    ds40=ds.sel(lat=domain['lat1'],method='nearest', drop=True).PSL.mean(dim='lon')
    ds65=ds.sel(lat=domain['lat2'],method='nearest', drop=True).PSL.mean(dim='lon')
    
    samIndex=xarray.Dataset(coords={"time":ds.time})
    
        #filter by the climatology
    ds40Climatology = climat.dateInterval(ds40, climatStart, climatFinish).groupby('time.month')
        #filter by the climatology
    ds65Climatology = climat.dateInterval(ds65, climatStart, climatFinish).groupby('time.month')
        
    samIndex['sam']=climat.normalise(ds40,ds40Climatology)-climat.normalise(ds65,ds65Climatology)
    
    return samIndex