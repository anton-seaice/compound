#This is multi-dimensional array handling
import xarray
import numpy




def decodeTime(ds):
    # Ref http://xarray.pydata.org/en/stable/weather-climate.html

    dates = xarray.cftime_range(start="0850", periods=13872, freq="MS", calendar="noleap")
       
    ds=ds.assign_coords(time=("time",dates))
        
    return ds

