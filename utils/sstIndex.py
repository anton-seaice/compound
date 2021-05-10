import xarray
import cftime

import sys
sys.path.append('../')
import utils._indexDefinitions as _index
import utils.climatology as climat


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

def calculateIndex(ds, climatStart, climatFinish):
    """
    This function calculates an area-average for the indeces specified in _indexDefitions based on monthly climatology.
    
    inputs:
    
    xarray ds in CESM format
    start and finish years to use a climatology
    
    output:
    
    new xarray with time dimension
        
    """

    
    # For now, assume this is CESM output. Although CMIP should be principally the same non?
    #list of index names, as defined in _indexDefitions file
    index = _index.sstIndex
    
    #There's only one depth dimension, so we will drop that
    ds['SST']=ds.SST.isel(z_t=0)

    #For some reason TAREA has a time demension, but doesn't change in time, so well drop that too
    ds['TAREA']=ds.TAREA.isel(time=0)

    #Making TAREA a coordinate
    ds=ds.set_coords('TAREA')
    
    #Create a dataset to add the results to
    resultDs = xarray.Dataset(coords={"time":ds.time})
    
    #for every index name
    for key in index:
        
        #grab the area of interest for this index
        domain=index[key]

        #Carve out the area of interest for this index
        #https://www.cesm.ucar.edu/models/ccsm3.0/csim/RefGuide/ice_refdoc/node9.html describes TLAT/TLONG. They are in the middle of a grid square in the model.
        domainDs=ds.where(
            (ds.TLAT>domain['latMin']) & (ds.TLAT<domain['latMax']) & (ds.TLONG>domain['longMin']) & (ds.TLONG<domain['longMax']),
            drop=True
        ).SST

        # First calculate the data range to use for climatology 
        domainSstClimat=climat.dateInterval(domainDs, climatStart,climatFinish)
        
        #calculate the monthly means of that range
        sstMean = domainSstClimat.groupby('time.month', restore_coord_dims=True).mean(dim='time')
           
        # caluclate the sst anomolies 
        domainDs['sstAnom']=domainDs.groupby(
            'time.month', restore_coord_dims=True
        )-sstMean

        #Then calculate a weighted mean
        #easternSstAv=(nino34.sstAnom*nino34.TAREA).sum(dim=('nlat','nlon'))/nino34.TAREA.sum()
        resultDs[key]=domainDs.sstAnom.weighted(domainDs.TAREA).mean(dim=('nlon','nlat'))
                
    # Special case for iod
    resultDs['dmi'] = resultDs['westIO'] - resultDs['eastIO']
       
    return resultDs
