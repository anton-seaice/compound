import cftime
import xarray

def dateInterval(x, climatStart, climatFinish):
    """Return an xarray sliced by the year range provided
    
    Inputs:
    x : an xarray ds/da
    climatStart: the start year
    climatFInish: the finish year
    
    """
    xClimatology=x.sel(
        time=slice(
            cftime.DatetimeNoLeap(climatStart,1,1),
            cftime.DatetimeNoLeap(climatFinish+1,1,1)
        )
    )     
    return xClimatology

def normalise(x, xClimatology):
    """This function calculates a normalised (by month) xarray for the provided range of years.
    
    Normalise in this case means to calculate anomalies and then make it all relative to the st.dev for that month.
    
    x is a valid xarray variable with a time coordinate
    xClimatology is the xarray of the time range to use for climatology
       
    """
    x=x.chunk({'time':'auto'})
    
    xMonthly = x.groupby('time.month')
    
    xClimatologyMean = xClimatology.groupby('time.month').mean(dim='time')
   
    # Use the calculated climatology to calculate the anomaly and the standard deviation
    xAnom=(xMonthly-xClimatologyMean).groupby('time.month')
    xStd=xClimatology.groupby('time.month').std(dim='time')
    
    
    return xAnom/xStd