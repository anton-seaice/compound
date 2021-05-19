import sys
sys.path.append('../')
import utils._indexDefinitions as _index

import xarray
import numpy
import cftime


def averageForTimePeriod(indexXr):
    """
    calculates the averages for the period of interest defined in _indexDefitions for the indeces in _indexDefinitions
    
    indexXr is a xarray
    
 """

    yearRange = numpy.arange(
        indexXr.time[0].dt.year,  #firstYear
        indexXr.time[-1].dt.year) #lastYear
    
    #we are interested indices which we have defined months of Interest for and are in the data
    indexNames = list(set(list(_index.monthsOfInterest)).intersection(list(indexXr.keys())))
  
    print(indexNames)
    
    #somewhere to write the answer
    answer = list()

    # for each index
    for keys in indexNames:
        #get the first and last month from _indexDefinitions
        months=(_index.monthsOfInterest[keys])
        
        # if the period is within one year
        if months[1]<12:
                answer.append(
                    xarray.concat(
                        [indexXr[keys].sel(
                            time=slice(
                                cftime.DatetimeNoLeap(year,months[0],1),
                                cftime.DatetimeNoLeap(year,months[1]+1,1)
                            )
                        ).mean() for year in yearRange], 
                        'year')
                    )
        # if the period goes over two years
        else:
                answer.append(
                    xarray.concat(
                        [indexXr[keys].sel(
                            time=slice(
                                cftime.DatetimeNoLeap(year,months[0],1),
                                cftime.DatetimeNoLeap(year+1,months[1]-11,1)
                            )
                        ).mean() for year in yearRange], 
                        'year')
                     )
    # merge the variables (indeces) back together
    results = xarray.merge(answer)
    results.year=yearRange
    results = results.assign_attrs(indexXr.attrs)
    
    return results
    






