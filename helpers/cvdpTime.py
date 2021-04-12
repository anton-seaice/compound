#This is multi-dimensional array handling
import xarray

import cftime

from dateutil.relativedelta import *

def decodeTime(ds):
    
    if ds.time.units == 'months since 850-01-15 00:00:00':
        newDate=[]
        startDate=datetime(850, 1,15)
        for i in ds.time.values:
            newDate.append(startDate+relativedelta(months=+int(i))
        
       decodedTimes=cftime.date2num(newDate, 'days since 850-01-15 00:00:00', calendar='standard') 
       attrs = {'units': 'days since 850-01-15 00:00:00', 'calendar': 'standard'}
       dates = xarray.Dataset({'time': ('time', decodedTimes, attrs)})
       dates = xarray.decode_cf(dates)
       ds.update({'time':('time', dates['time'], attrs)})
    
    return xa

