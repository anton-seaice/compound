#!/usr/bin/env python
# coding: utf-8

# In[4]:


#import my functions
import sys
sys.path.append('../')
import utils._indexDefinitions as _index


# In[5]:


import xarray
import numpy
import cftime
import pandas


# In[3]:


def averageForTimePeriod(indexXr):
    """calculates the averages for the period of interest defined in _indexDefitions for the indeces in _indexDefinitions
    
    
    indexXr is a xarray
    
    returns a pandas Dataframe. (You can cast this into an xarray is desired pretty easily: xarray.Dataset(result))"""
    #Figuring out the first and last year in the data set is more complicated than it should be. Here goes.

    firstYear = indexXr.time[0].dt.year
    lastYear = indexXr.time[-1].dt.year
    yearRange = numpy.arange(indexXr.time[0].dt.year,indexXr.time[-1].dt.year)
    
   

    #get a list of index names to iterate, 
    indexNames = list(_index.monthsOfInterest.keys())

    #ds = xarray.Dataset()
    results = pandas.DataFrame(index=yearRange)
    results.index.name='year'

    for keys in _index.monthsOfInterest:
        #get the first and last month from _indexDefinitions
        months=_index.monthsOfInterest[keys]
        
        #a list to populate in the next loop. First append everything to this list, and then add to the output dataframe
        answer = list()
        
        # if the period is within one year
        if months[1]<12:
            for year in yearRange:
                periodOfInterest=xarray.cftime_range(start=cftime.DatetimeNoLeap(year,months[0],1), 
                    end= cftime.DatetimeNoLeap(year,months[1]+1,1), 
                                                     freq='M')
                answer.append(float(indexXr[keys].sel(time=periodOfInterest).mean().values))
        # if the period goes over two years
        else:
            for year in yearRange:
                periodOfInterest=xarray.cftime_range(start=cftime.DatetimeNoLeap(year,months[0],1), 
                    end= cftime.DatetimeNoLeap(year+1,months[1]-12+1,1), 
                                                     freq='M')
                answer.append(float(indexXr[keys].sel(time=periodOfInterest).mean().values))
        
        # write the list into the dataframe
        results[keys]=answer

    return results
    


# In[ ]:




