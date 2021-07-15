import xarray
import cftime
import re
import numpy

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
        (ds.lat>domain['latMin']) & (ds.lat<domain['latMax']) & (ds.lon>domain['longMin']) & (ds.lon<domain['longMax']),
        drop=True
    ).SST

    return domainDs

def calculateClimatology(climatDs, *args): 
    """From a provided dataset, start year and finish year, return the calculated mean for every SST index defined in _indexDefinitions file.
    
    
    Useage
    calculateClimatology(climatDs) #calculates for all years
    
    Or to use a subset of the years
    calculateClimatology(climatDs, climatStart, climatFinish)
    
    """

    #Figure out what sort of data it is
    if (hasattr(climatDs, 'project_id')):
        if (climatDs.project_id=='CMIP'):
            #print('Ds looks like CMIP')
            #Rename it to look like CESM data
            #climatDs=climatDs.rename_dims({'lat':'nlat', 'lon':'nlon'})
            climatDs=climatDs.rename_vars({'tos':'SST',
                                           #'areacella':'TAREA', 
                                           #'lat':'TLAT', 'lon':'TLONG'
                                          })
    else:
        climatDs['SST']=climatDs.SST.isel(z_t=0)
   
    index = _index.sstIndex
    
    #DataFrame to put monthly sst means in 
    sstMean = dict()
       
    #for every index name
    for key in index:
        
        domainDs=sstDomain(climatDs, key)
        
        if len(args)==2:
            #reduce domain by years provided
            domainDs=climat.dateInterval(domainDs, args[0], args[1])
        elif len(args)!=0:
            raise(Error("Wrong number of inputs provided"))

        #calculate the monthly means of that range
        sstMean[key] = domainDs.groupby('time.month', restore_coord_dims=True).mean(dim='time')
        
      
    return sstMean

def calculateIndex(ds, *args):
    """
    This function calculates an area-average for the indeces specified in _indexDefitions based on monthly climatology.
    
    It also calculates a detrended version detrending based on global sst from -20 to +20 latitudes
    
    inputs:
    
    xarray ds to use for index calculationin CESM format
    args are either:
        start and finish years to use for climatology
        or an xarray climatDs to use for climatology (if different to the main dataset)

    output:
    
    new xarray with time dimension
        
    """

    #Input checking
    if len(args)==1:
        regex=re.compile('dict')
        if regex.search(str(type(args[0])))!=None:
            climatDs=args[0]
        else:
            raise(EnvironmentError("Climatology Ds provided is not a dict"))
    elif len(args)!=2:
        raise(EnvironmentError("Wrong input arguments provided"))
    
    #tidy up input data so the variable names are common between CMIP and CESM
    if (hasattr(ds, 'project_id')):
        if (ds.project_id=='CMIP'):
            #print('Ds looks like CMIP')
            #ds=ds.rename_dims({'lat':'nlat', 'lon':'nlon'})
            ds=ds.rename_vars({'tos':'SST',
                               #'areacella':'TAREA',
                               #'lat':'TLAT', 'lon':'TLONG'
                              })
    else:
        print('Ds looks like CESM') #CESM-LME
        #There's only one depth dimension, so we will drop that
        ds['SST']=ds.SST.isel(z_t=0)
        if ds.TAREA.dims=='time':
            #For some reason TAREA has a time dimension (possible from opening multiple files), but doesn't change in time, so well drop that too
            ds['TAREA']=ds.TAREA.isel(time=0)
    
    
    #Making TAREA a coordinate
    #ds=ds.set_coords('TAREA')

    #Create a dataset to add the results to
    resultDs = xarray.Dataset(coords={"time":ds.time})
    
    #list of index names, as defined in _indexDefitions file
    index = _index.sstIndex
    
    #for every index name
    for key in index:
        
        #find the area relevant for this index
        domainDs=sstDomain(ds, key)

        #if there were two arguments given for climatology, use the same data
        if len(args)==2:
                domainSstClimat=climat.dateInterval(domainDs, int(args[0]), int(args[1]))
                sstIndexMean = domainSstClimat.groupby('time.month', restore_coord_dims=True).mean(dim='time')
        else:
            #otherwise, use the provided climatology
            sstIndexMean=climatDs[key]
        
        # caluclate the sst anomolies 
        sstAnomDs=domainDs.groupby('time.month', restore_coord_dims=True
        )-sstIndexMean

        # to calculate an area weight average, using TAREA is best, but lots of data sets don't seem to have this, so weighting by the cosine of the latitude
        #http://xarray.pydata.org/en/stable/examples/area_weighted_temperature.html
        weights=numpy.cos(numpy.deg2rad(domainDs.lat))
        #weights=domainDs.TAREA
        
        #Then calculate a weighted mean
        resultDs[key+'NoDetrend']=sstAnomDs.weighted(weights).mean(dim=('lon','lat'))
        
        
    # Special case for iod
    resultDs['dmi'] = resultDs['westIONoDetrend'] - resultDs['eastIONoDetrend']
        
    #for every index name
    for key in index:
        # detrended weighted mean
        resultDs[key] = resultDs[key+'NoDetrend'] - resultDs['backgroundSstNoDetrend']
        
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
