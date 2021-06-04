
import xarray

import sys
sys.path.append(sys.path[0] + '/..')
import utils._indexDefinitions as _index



def applyCriteria(indexDa, critDa):
    """This function applies the criteria to the indeces provided to determine if the events are negative or positive events.
    
    Then it sums events which are fire promoting or not-fire promoting.
    
    Should return two dataArrays with the count of fire Promoting and non fire Promoting modes for the models and years in the input data.
    
    """
    
    #enso and iod events are positive, sam events are negative
    indexNames=list(critDa.variables)
    
    firePos=list(set(_index.firePos).intersection(indexNames))
    fireNeg=list(set(_index.fireNeg).intersection(indexNames))

    #events are greater than or less than the criteria
    #doing a comparison with a Nan retruns false, when its easier if its still a Nan, so put the where in to look for nans
    posEvents=(indexDa>critDa).where(indexDa.isnull()!=True)
    negEvents=(indexDa<-1*critDa).where(indexDa.isnull()!=True)
    
    # a positive impact is a positive event with a positive impact, or a negative event with a negative impact
    firePosDa=xarray.merge(
        [posEvents[firePos], negEvents[fireNeg]]
        )
    
    # a negative impact is a negative event with a positive impact, or a positive event with a negative impact
    fireNegDa=xarray.merge(
        [negEvents[firePos],posEvents[fireNeg]]
    )
    
    return firePosDa, fireNegDa    



def compound(fireDa):
    """
    
    
    For now, assuming there are only three indeces being assessed, more should be possible, but not in scope
    
    """

    #Which indices are we using?
    indexNames=list(fireDa.variables)

    ensoIndex=(set(_index.enso).intersection(indexNames))
    iodIndex=(set(_index.iod).intersection(indexNames))
    samIndex=(set(_index.sam).intersection(indexNames))

    indexNames=[*ensoIndex, *iodIndex, *samIndex]
    
    #For now, limiting ourselves to one for each driver
    if len(ensoIndex)!=1:
        raise Error('number of enso indeces is not 1')
    elif len(iodIndex)!=1:
        raise Error('number of iod indeces is not 1')
    elif len(samIndex)!=1:
        raise Error('number of sam indeces is not 1')

    #How many events were there in each year?
    #convert to an Da, so we can sum over the variables
    fireDs=fireDa[indexNames].to_array()
    #number of events is the sum of the three variables, but only where none of them are Nan
    fireDa['nEvents']=fireDs.sum(dim='variable').where(
        fireDs.isnull().all(dim='variable')!=True
    )
     
    #Which years are there all three
    fireDa['all3']=(fireDa.nEvents==3).where(
        fireDa.nEvents.isnull()!=True
    )
    
    fireDa=fireDa.assign_attrs({**fireDa.attrs, 'all3':str(indexNames)})

    #Something to iterate names of pairs into
    pairs=list()
    
    #Match each index with those further along the index list
    #(Nested for loops are probably bad juju)
    for i1 in range(0,len(indexNames)):
        for i2 in range(i1+1, len(indexNames)):
            #Its a compound of those two, if they both occur, and excluding if its a compound of all three
            fireDa[indexNames[i1]+'+'+indexNames[i2]]=(
                fireDa[indexNames[i1]]*
                fireDa[indexNames[i2]]*
                (fireDa['all3']==False)
            )
            
            pairs.append(indexNames[i1]+'+'+indexNames[i2])
            
    #drop compounds from individual indices
    fireDa[indexNames]=xarray.where(fireDa.nEvents.isnull(), float('NaN'),
                                    xarray.where(fireDa.nEvents==1, fireDa[indexNames], 0)
                                   ) #horrorshow?
    
    fireDa['anyCompound']=xarray.where(fireDa.nEvents.isnull(), float('NaN'), (fireDa.nEvents>1).astype('int') )
            
    #Write the names of pairs into attributes for neatness
    fireDa=fireDa.assign_attrs({**fireDa.attrs,'indeces':indexNames, 'pairs':pairs})
            
    return fireDa







