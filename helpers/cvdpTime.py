#This is multi-dimensional array handling
import xarray

import pandas

def decode(xa):
    
    if xa.time.units == 'months since 850-01-15 00:00:00':
        xa.time['date'] = pandas.period_range(start='850-01-15', periods=len(xa.time), freq='M')
    
    return xa

