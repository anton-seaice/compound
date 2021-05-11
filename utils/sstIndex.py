import xarray
import cftime
import re

import sys
sys.path.append('../')
import utils._indexDefinitions as _index
import utils.climatology as climat


def sstDomain(ds, indexKey):
    """From a provided dataset, return the area domain of sea surface temperatures for the index request """
    
    #grab the area of interest for this index
    domain=_index.sstIndex[indexKey]

    #ADD RANGE CHECKING!
    
    #Carve out the area of interest for this index
    #https://www.cesm.ucar.edu/models/ccsm3.0/csim/RefGuide/ice_refdoc/node9.html describes TLAT/TLONG. They are in the middle of a grid square in the model.
    domainDs=ds.where(
        (ds.TLAT>domain['latMin']) & (ds.TLAT<domain['latMax']) & (ds.TLONG>domain['longMin']) & (ds.TLONG<domain['longMax']),
        drop=True
    ).SST

    return domainDs

def calculateClimatology(climatDs, climatStart, climatFinish): 
    """From a provided dataset, start year and finish year, return the calculated mean for every SST index defined in _indexDefinitions file."""
    
    climatDs['SST']=climatDs.SST.isel(z_t=0)
   
    index = _index.sstIndex
    
    #DataFrame to put monthly sst means in 
    sstMean = dict()
       
    #for every index name
    for key in index:
        
        domainDs=sstDomain(climatDs, key)
        
        domainSstClimat=climat.dateInterval(domainDs, climatStart, climatFinish)      

        #calculate the monthly means of that range
        sstMean[key] = domainSstClimat.groupby('time.month', restore_coord_dims=True).mean(dim='time')
        
      
    return sstMean

def calculateIndex(ds, *args):
    """
    This function calculates an area-average for the indeces specified in _indexDefitions based on monthly climatology.
    
    It also calculates a detrended version detrending based on global sst from -20 to +20 
    
    inputs:
    
    xarray ds to use for index calculationin CESM format
    args are either:
        start and finish years to use for climatology
        or an xarray climatDs to use for climatology (if different to the main dataset)

    output:
    
    new xarray with time dimension
        
    """

    if len(args)==1:
        regex=re.compile('dict')
        if regex.search(str(type(args[0])))!=None:
            climatDs=args[0]
        else:
            raise(EnvironmentError("Climatology Ds provided is not a dict"))
    elif len(args)!=2:
        raise(EnvironmentError("Wrong input arguments provided"))
    
    # For now, assume this is CESM output. Although CMIP should be principally the same non?
    #list of index names, as defined in _indexDefitions file
    index = _index.sstIndex
    
    #There's only one depth dimension, so we will drop that
    ds['SST']=ds.SST.isel(z_t=0)

    if ds.TAREA.dims=='time':
        #For some reason TAREA has a time dimension (possible from opening multiple files), but doesn't change in time, so well drop that too
        ds['TAREA']=ds.TAREA.isel(time=0)

    #Making TAREA a coordinate
    ds=ds.set_coords('TAREA')
    
    #Create a dataset to add the results to
    resultDs = xarray.Dataset(coords={"time":ds.time})
    
    #for every index name
    for key in index:
        
        domainDs=sstDomain(ds, key)

        #if there were two arguments given for climatology, use the same data
        if len(args)==2:
            try:
                domainSstClimat=climat.dateInterval(domainDs, int(args[0]), int(args[1]))
                
                sstIndexMean = domainSstClimat.groupby('time.month', restore_coord_dims=True).mean(dim='time')
       
            except:
                #There is an assumption here the error is that in couldn't cast the inputs to int
                raise(EnvironmentError("Input Year Range not recognised"))
        else:
            sstIndexMean=climatDs[key]
        
        # caluclate the sst anomolies 
        domainDs['sstAnom']=domainDs.groupby(
            'time.month', restore_coord_dims=True
        )-sstIndexMean

        #Then calculate a weighted mean
        #easternSstAv=(nino34.sstAnom*nino34.TAREA).sum(dim=('nlat','nlon'))/nino34.TAREA.sum()
        resultDs[key+'NoDetrend']=domainDs.sstAnom.weighted(domainDs.TAREA).mean(dim=('nlon','nlat'))
                
    # Special case for iod
    resultDs['dmi'] = resultDs['westIO'] - resultDs['eastIO']
    
        #for every index name, calculate a detrended version too
    for key in index:
        resultDs[key] = resultDs[key+'NoDetrend'] - resultDs['backgroundSst']
       
    return resultDs


def plotArea(ds) :
    """
        #Sanity check the area looks believable ?
        nino34Slice = ds.isel(time=0) # select a slice

        # -- plot the 'quick' way
        plt.figure(figsize=(8,4))
        ax = plt.axes(projection=ccrs.Robinson(central_longitude=160))  # set up projection
        ax.set_global()

        #sst2d.SST.plot.pcolormesh()

        nino34Slice.SST.plot.pcolormesh(ax=ax, transform=ccrs.PlateCarree(), x='TLONG', y='TLAT', center=False, levels=35)


        ax.coastlines()
        ax.gridlines()
        plt.show()"""
    
    return
