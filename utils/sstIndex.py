import xarray
import cftime

import sys
sys.path.append('../')
import utils._indexDefinitions as _index

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
    
    output:
    
    new xarray with time dimension
        
    """

    
    # For now, assume this is CESM output. Although CMIP should be principally the same non?
    
    index = _index.sstIndex
    
    #There's only one depth dimension, so we will drop that
    ds['SST']=ds.SST.isel(z_t=0)

    #For some reason TAREA has a time demension, but doesn't change in time, so well drop that too
    ds['TAREA']=ds.TAREA.isel(time=0)

    #Making TAREA a coordinate
    ds=ds.set_coords('TAREA')
    
    resultDs = xarray.Dataset(coords={"time":ds.time})
    
    for key in index:

        
        #grad the area of interest for this index
        domain=index[key]

        #Carve out the area of interest for this domain
        #https://www.cesm.ucar.edu/models/ccsm3.0/csim/RefGuide/ice_refdoc/node9.html describes TLAT/TLONG. They are in the middle of a grid square in the model.
        domainDs=ds.where((ds.TLAT>domain['latMin']) & (ds.TLAT<domain['latMax']) & (ds.TLONG>domain['longMin']) & (ds.TLONG<domain['longMax']), drop=True)

        # First calculate SST Anomalies based on
        # climatology = "850-2005 climatology removed prior to all calculations (other than means)";
        domainSst=domainDs.sel(
            time=slice(
                cftime.DatetimeNoLeap(climatStart,1,1),
                cftime.DatetimeNoLeap(climatFinish+1,1,1)
            )
        ).SST.groupby(
            'time.month', restore_coord_dims=True
        )
            
        domainDs['sstAnom']=domainSst-domainSst.mean(dim='time')

        #Then calculate a weighted mean
        #easternSstAv=(nino34.sstAnom*nino34.TAREA).sum(dim=('nlat','nlon'))/nino34.TAREA.sum()
        resultDs[key]=domainDs.sstAnom.weighted(domainDs.TAREA).mean(dim=('nlon','nlat'))
        
        """
        #This could be an alternative way to calculate the area weighting
        # Ref: http://xarray.pydata.org/en/stable/examples/area_weighted_temperature.html

        nino34['weights']=numpy.cos(numpy.deg2rad(nino34.TLAT))

        domainAreaTotal=nino34.weights.sum()

        #domainAv=(nino34.sstAnom*nino34.weights).sum(dim=('nlat','nlon'))/domainAreaTotal

        domainAv=nino34.sstAnom.weighted(nino34.weights).mean(dim=('nlon','nlat'))
        """
        
    # Special case for iod
    resultDs['indian_ocean_dipole'] = resultDs['westIO'] - resultDs['eastIO']
       
    return resultDs