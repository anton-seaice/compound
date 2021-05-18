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




def averageForTimePeriod(indexXr):
    """calculates the averages for the period of interest defined in _indexDefitions for the indeces in _indexDefinitions
    
    
    indexXr is a xarray
    
    returns a pandas Dataframe. (You can cast this into an xarray is desired pretty easily: xarray.Dataset(result))"""

    firstYear = indexXr.time[0].dt.year
    lastYear = indexXr.time[-1].dt.year
    yearRange = numpy.arange(indexXr.time[0].dt.year,indexXr.time[-1].dt.year)
    
    indexNames = list(set(list(_index.monthsOfInterest)).intersection(list(indexXr.keys())))
  
    print(indexNames)
    
    #somewhere to write the answer
    answer = numpy.ndarray([len(yearRange),len(indexNames)])
    


    
    #month=numpy.ndarray([len(indexNames),2])

    for iKey in numpy.arange(0,len(indexNames)):
        #get the first and last month from _indexDefinitions
        months=(_index.monthsOfInterest[indexNames[iKey]])
        keys=indexNames[iKey]
        
        # if the period is within one year
        if months[1]<12:
            for year in yearRange:
                periodOfInterest=xarray.cftime_range(
                    start=cftime.DatetimeNoLeap(year,months[0],1), 
                    end= cftime.DatetimeNoLeap(year,months[1]+1,
                                               1), 
                                                     freq='M')
                answer[year-yearRange[0],iKey]=(float(indexXr[keys].sel(time=periodOfInterest).mean().values))
        # if the period goes over two years
        else:
            for year in yearRange:
                periodOfInterest=xarray.cftime_range(
                    start=cftime.DatetimeNoLeap(year,months[0],1), 
                    end= cftime.DatetimeNoLeap(year+1,months[1]-12+1,
                                               1), 
                                                     freq='M')
                answer[year-yearRange[0],iKey]=(float(indexXr[keys].sel(time=periodOfInterest).mean().values))
        
        # write the list into the dataframe
        
    results = pandas.DataFrame(data=answer, index=yearRange, columns=indexNames)
    results.index.name='year'
    results[keys]=answer

    return results
    






