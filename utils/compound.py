
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
    print('firePos: ')
    print(firePos)
    fireNeg=list(set(_index.fireNeg).intersection(indexNames))
    print('fireNeg: ')
    print(fireNeg)
    
    #events are greater than or less than the criteria
    #doing a comparison with a Nan retruns false, when its easier if its still a Nan, so put the where in to look for nans
    posEvents=(indexDa>critDa).where(indexDa.isnull()!=True, drop=True)
    negEvents=(indexDa<-1*critDa).where(indexDa.isnull()!=True, drop=True)
    
    # a positive impact is a positive event with a positive impact, or a negative event with a negative impact
    firePosDa=xarray.merge(
        [posEvents[firePos], negEvents[fireNeg]]
        )
    
    # a negative impact is a negative event with a positive impact, or a positive event with a negative impact
    fireNegDa=xarray.merge(
        [negEvents[firePos],posEvents[fireNeg]]
    )
    
    return firePosDa, fireNegDa    



def compound(inputDa):
    """
    
    
    For now, assuming there are only three indeces being assessed, more should be possible, but not in scope
    
    """

    #Which indices are we using?
    indexNames=list(inputDa.variables)

    ensoIndex=(set(_index.enso).intersection(indexNames))
    iodIndex=(set(_index.iod).intersection(indexNames))
    samIndex=(set(_index.sam).intersection(indexNames))

    #indexNames=[*ensoIndex, *iodIndex, *samIndex]
    
    #For now, limiting ourselves to one for each driver
    if len(ensoIndex)==0:
        raise EnvironmentError('no enso indeces found')
    elif len(iodIndex)==0:
        raise EnvironmentError('no iod indeces found')
    elif len(samIndex)==0:
        raise EnvironmentError('no sam indeces found')
        
    indexSets=dict()
    #nest for loops are the besssttt
    for iEnso in ensoIndex:
        for iIod in iodIndex:
            for iSam in samIndex:
                indexSets[iEnso+iIod.capitalize()+iSam.capitalize()]=[iEnso,iIod,iSam]
                
               
    allFireLs=list()
            
    for iSet in indexSets.keys():

        print(iSet)
        indexNames=indexSets[iSet]
        fireDa=xarray.Dataset()
        
        #How many events were there in each year?
        #convert to an Ds, so we can sum over the variables
        fireDs=inputDa[indexNames].to_array()
        #number of events is the sum of the three variables, but only where none of them are Nan
        fireDa['nEvents']=fireDs.sum(dim='variable').where(
            fireDs.isnull().all(dim='variable')!=True
        )

        #Which years are there all three
        fireDa['all3']=(fireDa.nEvents==3).where(
            fireDa.nEvents.isnull()!=True
        )
        
        #Something to iterate names of pairs into
        #pairs=list()

        #Match each index with those further along the index list
        #(Nested for loops are probably bad juju)
        #for i1 in range(0,len(indexNames)):
        #    for i2 in range(i1+1, len(indexNames)):
        #        #Its a compound of those two, if they both occur, and excluding if its a compound of all three
        #        fireDa[indexNames[i1]+'+'+indexNames[i2]]=(
        #            fireDa[indexNames[i1]]*
        #            fireDa[indexNames[i2]]*
        #            (fireDa['all3']==False)
        #        )
        #        pairs.append(indexNames[i1]+'+'+indexNames[i2])

        fireDa['enso+iod']=(inputDa[indexNames[0]]*inputDa[indexNames[1]]*(fireDa['all3']==False))
        fireDa['enso+sam']=(inputDa[indexNames[0]]*inputDa[indexNames[2]]*(fireDa['all3']==False))
        fireDa['iod+sam']=(inputDa[indexNames[1]]*inputDa[indexNames[2]]*(fireDa['all3']==False))
        
        pairs=['enso+iod','enso+sam','iod+sam']
        
        #drop compounds from individual indices
        fireDa['enso']=xarray.where(fireDa.nEvents.isnull(), float('NaN'),
                                        xarray.where(fireDa.nEvents==1, inputDa[indexNames[0]], 0)
                                       ) 
        fireDa['iod']=xarray.where(fireDa.nEvents.isnull(), float('NaN'),
                                        xarray.where(fireDa.nEvents==1, inputDa[indexNames[1]], 0)
                                       )
        fireDa['sam']=xarray.where(fireDa.nEvents.isnull(), float('NaN'),
                                        xarray.where(fireDa.nEvents==1, inputDa[indexNames[2]], 0)
                                       )#horrorshow?

        fireDa['anyCompound']=xarray.where(fireDa.nEvents.isnull(), float('NaN'), (fireDa.nEvents>1).astype('int') )
        
        allFireLs.append(fireDa.to_array(dim='compound', name=iSet))
            
            
    outputXr = xarray.merge(allFireLs)
    outputXr=outputXr.assign_attrs({'indeces':indexNames, 'pairs':pairs, 'others':['all3','anyCompound','nEvents']})
    
    return outputXr






