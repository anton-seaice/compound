import cftime
import xarray



def dateInterval(x, climatStart, climatFinish):

    
    # Calculate the climatology for the provided years
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
    
    # First group into months
    xMonthly=x.groupby('time.month')

    # Use the calculated climatology to calculate the anomaly and the standard deviation
    xAnom=(xMonthly-xClimatology.mean(dim='time')).groupby('time.month')
    xStd=xClimatology.std(dim='time')
    
    return xAnom/xStd