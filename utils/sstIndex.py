import xarray


def calculateIndex(ds, index):
    """
    
    
    
    """

    
    # For now, assume this is CESM output. Although CMIP should be principally the same non?
    
 
    
    #There's only one depth dimension, so we will drop that
    ds['SST']=ds.SST.isel(z_t=0)

    #For some reason TAREA has a time demension, but doesn't change in time, so well drop that too
    ds['TAREA']=ds.TAREA.isel(time=0)

    #Making TAREA a coordinate
    ds=ds.set_coords('TAREA')
    
    for key in index:

        domain=index[key]

        #Carve out the area of interest for nino 34
        #https://www.cesm.ucar.edu/models/ccsm3.0/csim/RefGuide/ice_refdoc/node9.html describes TLAT/TLONG. They are in the middle of a grid square in the model.
        domainDs=ds.where((ds.TLAT>domain['latMin']) & (ds.TLAT<domain['latMax']) & (ds.TLONG>domain['longMin']) & (ds.TLONG<domain['longMax']), drop=True)

        # First calculate SST Anomalies based on
        # climatology = "850-2005 climatology removed prior to all calculations (other than means)";
        domainSst=domainDs.SST.groupby('time.month')    
        domainDs['sstAnom']=domainSst-domainSst.mean(dim='time')

        #Then calculate a weighted mean
        #easternSstAv=(nino34.sstAnom*nino34.TAREA).sum(dim=('nlat','nlon'))/nino34.TAREA.sum()
        ds[key]=domainDs.sstAnom.weighted(domainDs.TAREA).mean(dim=('nlon','nlat'))
    
    return ds