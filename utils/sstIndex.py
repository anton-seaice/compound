import xarray
import cftime
import re
import numpy

import sys
sys.path.append('../')
import utils._indexDefinitions as _index
import utils.climatology as climat


def sstDomain(ds, indexKey):
    """From a provided xarray, return the area domain of sea surface temperatures for the index requested 
    
    the xarray must have lon and lat coordinates
    
    the string indexKey must be defined in utils/_indexDefinitions.py as a sstIndex
    
    """
    
    #grab the area of interest for this index
    try:
        domain=_index.sstIndex[indexKey]
    except:
        raise EnvironmentError(indexKey + " not defined in utils/_indexDefinitions.py file as a sst domain")
        
    #there is no range checking if the areas defined are non-sense. this would be complicated because there is no particular requirement on the range, as long as it is consistent with how it is defined in indexDefinitions. (i.e. if your file has -150E, but you definition uses 330E, it won't work properly but won't report an error)
    
    #Carve out the area of interest for this index
    #https://www.cesm.ucar.edu/models/ccsm3.0/csim/RefGuide/ice_refdoc/node9.html describes TLAT/TLONG. They are in the middle of a grid square in the model.
    domainDs=ds.where(
        (ds.lat>domain['latMin']) & (ds.lat<domain['latMax']) & (ds.lon>domain['longMin']) & (ds.lon<domain['longMax']),
        drop=True
    )

    return domainDs

def calculateClimatology(climatDs, *args): 
    """From a provided sea surface temperature dataset, start year and finish year, return the calculated mean for every SST index defined in _indexDefinitions file.
    
    
    Useage
    calculateClimatology(climatDs) #calculates for all years
    
    Or to use a subset of the years
    calculateClimatology(climatDs, climatStart, climatFinish)
    
    """
    #indeces to calculate
    index = _index.sstIndex
    
    #DataFrame to put monthly sst means in 
    sstMean = dict()
       
    if len(args)==2:
        #reduce domain by years provided
        climatDs=climat.dateInterval(climatDs, args[0], args[1])
    elif len(args)!=0:
        raise(Error("Wrong number of inputs provided"))
    #else do nothing, 0 arguments provided means length the full length of the dataset
        
    #for every index name
    for key in index:
        
        #get the relevant area
        domainDs=sstDomain(climatDs, key)
        
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
    #if not(hasattr(ds, 'project_id')):
        #if (ds.project_id=='CMIP'):
            #print('Ds looks like CMIP')
            #ds=ds.rename_dims({'lat':'nlat', 'lon':'nlon'})
            #ds=ds.rename_vars({'tos':'SST',
                               #'areacella':'TAREA',
                               #'lat':'TLAT', 'lon':'TLONG'
             #                 })
    #else:
    #    print('Ds looks like CESM') #CESM-LME
    #    ds=ds.rename_vars({
    #                    'TLAT':'lat',
    #                    'TLONG':'lon'
    #                      })
    #    #There's only one depth dimension, so we will drop that
        #ds['SST']=ds.SST.isel(z_t=0)
    #    ds=ds.isel(z_t=0)
    #    if ds.TAREA.dims=='time':
            #For some reason TAREA has a time dimension (possible from opening multiple files), but doesn't change in time, so well drop that too
     #       ds['TAREA']=ds.TAREA.isel(time=0)
    
    
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
        dimsNotTime=set(sstAnomDs.dims).difference(['time'])
        resultDs[key+'NoDetrend']=sstAnomDs.weighted(weights).mean(dim=dimsNotTime)
        
        
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
