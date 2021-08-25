import xarray
import numpy

def binSum(da):
    """Return a da with the sum of events for each index given in overlaping 30 year bins, seperated at 10 year intervals"""

    #overlapping 30 year bins at 10 year intervals from 850 to 2100

    #first bin mid poitns is 865, and last is 2085

    #number of bins is (2085-865)/10 + 1 = 123

    #output is sum for each index of the number of events, for each interval and experiment

    #output a list of DA to then concatenate
    
    #a couple of vars to append to
    binMid=list()
    binSum=list()
    binN=list()

    #hardcoding these is lazy, but maybe fine
    startYear=int(da.year[0])
    endYear=int(da.year[-1])
    interval=10
    binSize=30

    numberOfBins=numpy.floor((endYear-startYear-binSize)/interval + 1)
    
    # for every bin
    for iBin in numpy.arange(0,numberOfBins):
        # firstYear is 850 + counter*30
        firstYear=startYear+iBin*interval
        # last year is 30 years after
        lastYear=firstYear+binSize
        # label/midPoint for bin
        binMid.append(int((firstYear+lastYear)/2))
        # calculate the sum for this year interval
        daInterval = da.sel(year=numpy.arange(firstYear,lastYear))
        binSum.append(
            daInterval.sum(dim='year').where(
                daInterval.isnull().any(dim='year')!=True
            )
        )

    #for the list of means, concat the results into a new xarray with new dimension 'year'
    overlapBinDa=xarray.concat(binSum, 'year')
    #populate the dimension year with the midpoint
    overlapBinDa=overlapBinDa.assign_coords(year=binMid)
    #add some attributes for reference
    overlapBinDa=overlapBinDa.assign_attrs({
        **da.attrs,
        'Bins':'Overlapping 30 year bins, seperating by 10 year intervals', 
        'Year':'Midpoint of bin'
    })

    return overlapBinDa



def binPlot(da):
    import matplotlib.pyplot as plt
    
    toPlot=['enso+iod', 'enso+sam', 'iod+sam','all3']
    colors=['orange', 'purple', 'green','blue']
    
    dims = list(da.coords)
    dims.remove('year')
    
    plt.figure(figsize=(18,6))

    for counter in range(0,len(toPlot)):
        plt.vlines(
            x=da.year-len(toPlot)+1.5*counter, 
            ymin=0,
            ymax=da[toPlot[counter]].mean(dims),
            label=toPlot[counter],
            color=colors[counter]
        )

    plt.legend(loc='upper left')
    plt.xticks(ticks=da.year)
    plt.xlabel('Mid-point of 30 year bin')
    plt.ylim(0,8)
    plt.ylabel('Number of events (mean)')
    #plt.title('Pairs and all-three for runs with ' + str(expSet))
    plt.minorticks_on()