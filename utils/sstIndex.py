import xarray

myDict = {
    "nino34" : {"latMin":-5, "latMax":5, "longMin":190,"longMax":240}
} #Need to move this to a seperate file that can be used across many test cases. (Probably a general _defines file.)


def calculateIndex(ds, indexName):
    """
    
    
    
    """

    
    # For now, assume this is CESM output. Although CMIP should be principally the same non?
    
    
    # giving this var a new name so as to not touch the original variable? Not sure this is how python actually works.
    domainDs=ds
    
    #There's only one depth dimension, so we will drop that
    domainDs['SST']=domainDs.SST.isel(z_t=0)

    #For some reason TAREA has a time demension, but doesn't change in time, so well drop that too
    domainDs['TAREA']=domainDs.TAREA.isel(time=0)

    #Making TAREA a coordinate
    domainDs=domainDs.set_coords('TAREA')
    
    domain=myDict[indexName]
    
    #Carve out the area of interest for nino 34
    domainDs=ds.where((ds.TLAT>=domain['latMin']) & (ds.TLAT<=domain['latMax']) & (ds.TLONG>=domain['longMin']) & (ds.TLONG<=domain['longMax']), drop=True)

    # First calculate SST Anomalies based on
    # climatology = "850-2005 climatology removed prior to all calculations (other than means)";
    domainSst=domainDs.SST.groupby('time.month')    
    domainDs['sstAnom']=domainSst-domainSst.mean(dim='time')
    
    #Then calculate a weighted mean
    #easternSstAv=(nino34.sstAnom*nino34.TAREA).sum(dim=('nlat','nlon'))/nino34.TAREA.sum()
    domainDs['nino34']=domainDs.sstAnom.weighted(domainDs.TAREA).mean(dim=('nlon','nlat'))
    
    return domainDs