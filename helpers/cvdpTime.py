import xarray
import numpy
import re
import cftime

def decodeTime(ds):
    """Convert time coordinates within xarray which are non-standard format to the xarray standard.
    
    In case of months since 850, it is converted to an array of cftime.datetime objects per xarray standard use. (The array is too long to use numpy.datetime64 data type.)
    
    Currently support xarray time units is:
        months since 850-01-15 00:00:00 (used by CESM CVDP)
    
        (Other time units could be added as needed)
    
    """
    
    # Ref http://xarray.pydata.org/en/stable/weather-climate.html

    # It appears that np.datetime64 supports the years 1678 to 2262. Maybe a rewrite to reflect that would be better.
    
    searchTerm=re.compile('months since ')
    
    # For CESM CVDP
    if searchTerm.match(ds.time.units):
    
        nPeriods=len(ds.time)
        start=ds.time.units.split(' ')[2]
        
        # Create an xarray of cftime.datetime objects
        dates = xarray.cftime_range(
            start=cftime.DatetimeNoLeap(
                int(start.split('-')[0]) ,
                int(start.split('-')[1]) ,
                int(start.split('-')[2]) , 
            ) ,
            periods=nPeriods, 
            freq="M", calendar="noleap")
       
    else:
        raise EnvironmentError('Time format no recognised')
    
    # Assign the new array to the time coordinate
    ds=ds.assign_coords(time=("time",dates))
        
    return ds

