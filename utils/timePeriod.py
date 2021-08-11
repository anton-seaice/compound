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
        indexXr.time[-1].dt.year #lastYear
    ) 
    
    #we are interested indices which we have defined months of Interest for and are in the data
    indexNames = list(set(list(_index.monthsOfInterest)).intersection(list(indexXr.variables)))
  
    if len(indexNames)==0:
        raise EnvironmentError('No indeces found in input data to calculate interval for')
    
    #somewhere to write the answer
    answer = list()

    # for each index
    for keys in indexNames:
        #get the first and last month from _indexDefinitions
        months=(_index.monthsOfInterest[keys])
        if isinstance(months,dict):
            season=list(months.keys())
        elif isinstance(months,list):
            season=['']
            months={'':months}
        else:
            raise EnvironmentError(keys+" months not specified as list or dict")
        
        for i in range(len(season)):
            iSeason=season[i]
            iMonths=months[iSeason]
            # if the period is within one year
            if any([
                iMonths[0]<0,
                iMonths[1]<iMonths[0]
            ]):
                raise EnvironmentError(keys+" months chosen non-sensical")
            elif iMonths[1]<12:
                answer.append(
                    xarray.concat(
                        [indexXr[keys].sel(
                            time=slice(
                                cftime.DatetimeNoLeap(year,iMonths[0],1),
                                cftime.DatetimeNoLeap(year,iMonths[1]+1,1)
                            )
                        ).mean(dim='time') for year in yearRange], 
                        'year')
                    )
            # if the period goes over two years
            else:
                answer.append(
                    xarray.concat(
                        [indexXr[keys].sel(
                            time=slice(
                                cftime.DatetimeNoLeap(year,iMonths[0],1),
                                cftime.DatetimeNoLeap(year+1,iMonths[1]-11,1)
                            )
                        ).mean(dim='time')  for year in yearRange], 
                        'year')
                     )
             
            answer[-1].name=(keys+iSeason.capitalize())
            
    # merge the variables (indeces) back together
    results = xarray.merge(answer)
    results['year']=yearRange
    results = results.assign_attrs(indexXr.attrs)
    
    return results
    






