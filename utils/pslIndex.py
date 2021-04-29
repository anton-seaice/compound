
import cftime

def normalisePSL(x, climatStart, climatFinish):
    """This function calculates a normalised (by month) PSL for the provided range of years.
    
    Normalise in this case means to calculate PSL anomalies and then make it all relative to the st.dev for that month.
    
    x is a valid xarray object with a PSL variable and a time coordinate
    climateStart is the start year
    climateFinish is the finish year
    
    
    TO DO: Convert climateStart and climatFinish to keyword arguments and make them optional ?"""
    
    # First group into months
    xMonthly=x.PSL.groupby('time.month')
    
    # Calculate the climatology for the provided years
    xClimatology=x.PSL.sel(
        time=slice(cftime.DatetimeNoLeap(climatStart,1,1),cftime.DatetimeNoLeap(climatFinish,12,1))
        ).groupby('time.month')
    
    # Use the calculated climatology to calculate the anomaly and the standard deviation
    xAnom=(xMonthly-xClimatology.mean(dim='time')).groupby('time.month')
    xStd=xClimatology.std(dim='time')
   
    return xAnom/xStd

def calculateSamIndex(ds, climatStart, climatFinish):
    
    ds40=ds.sel(lat=-40,method='nearest', drop=True).mean(dim='lon')
    ds65=ds.sel(lat=-65,method='nearest', drop=True).mean(dim='lon')
    samIndex=normalisePSL(ds40,climatStart, climatFinish)-normalisePSL(ds65,climatStart, climatFinish)
    samIndex.rename('sam')
    
    return samIndex