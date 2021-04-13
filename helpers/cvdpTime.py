import xarray
import numpy


def decodeTime(ds):
    """Convert time coordinates within xarray which are non-standard format to the xarray standard.
    
    In case of months since 850, it is converted to an array of cftime.datetime objects per xarray standard use. (The array is too long to use numpy.datetime64 data type.)
    
    Currently support xarray time units is:
        months since 850-01-15 00:00:00 (used by CESM CVDP)
    
        (Other time units could be added as needed)
    
    """
    
    # Ref http://xarray.pydata.org/en/stable/weather-climate.html

    # It appears that np.datetime64 supports the years 1678 to 2262. Maybe a rewrite to reflect that would be better.
    
    
    # For CESM CVDP
    if ds.time.units=='months since 850-01-15 00:00:00':
    
        nPeriods=len(ds.time)
        
        # Create an xarray of cftime.datetime objects
        dates = xarray.cftime_range(start="0850-01-15", periods=nPeriods, freq="MS", calendar="noleap")
       
    # Assign the new array to the time coordinate
    ds=ds.assign_coords(time=("time",dates))
        
    return ds

