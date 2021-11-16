#!/usr/bin/env python3
# coding: utf-8


# # 1. Calculate CMIP Indeces

# For each experiment in historical, calculate indices


#import my functions
import helpers.fileHandler as fh
import utils._modelDefinitions as _model
import utils._indexDefinitions as _index
import utils.sstIndex as sst
import utils.pslIndex as psl
import utils.timePeriod as tp
import utils.compound as compound


# other good functions
import xarray
import numpy
import matplotlib.pyplot as plt

# turn off warnings due to slicing warnings from xarray
import warnings
warnings.filterwarnings('ignore')

#experiments
deckSet=['piControl','historical']
scenarioSet=[#'ssp126', 'ssp245', 'ssp370',
             'ssp585']
experimentSet=[*deckSet, *scenarioSet]

#model names and variants
modelSet=_model.scenarioMip#[[22],:]

#indeces
sstIndeces = _index.sstIndex.keys()
pslIndeces = _index.pslIndex


def allIndexCalc(sstDs,sstClimat,pslDs,pslClimat):
    sstIndex = sst.calculateIndex(sstDs, sstClimat) 
    pslIndex, junk = psl.calculateSamIndex(pslDs, pslClimat)

    monthlyIndeces = xarray.merge([pslIndex, sstIndex])
    
    return monthlyIndeces

# Climatology and piControl:
for iModel in modelSet:
    
    print(iModel)
    
    try: 
        #calculate climatology
        
        print(iModel[1] + ' starting') 
        #SST
        tsDs = fh.loadModelData(iModel[1], 'tos_Omon', 'piControl', iModel[2]).tos
        controlDs=tsDs.assign_attrs({'project_id':'CMIP'})
        sstClimat=sst.calculateClimatology(controlDs)

        [sstClimat[i].to_netcdf('results/cmipMonthlyIndeces/sstTosClimat'+iModel[1]+i+'.nc')
             for i in sstIndeces]

        pslControlDs=fh.loadModelData(iModel[1], 'psl_Amon', 'piControl', iModel[2])
        pslClimat=psl.calculateClimatology(pslControlDs)

        pslClimat.to_netcdf('results/cmipMonthlyIndeces/pslClimat'+iModel[1]+'.nc')

    except Exception as e:
        print(iModel[1] + "Climatology did not calculate")
        print(e)


for iModel in modelSet:
    
    try:
        print(iModel)
        sstClimat=dict()

        for i in sstIndeces:
            sstClimat[i]=xarray.open_dataarray('results/cmipMonthlyIndeces/sstTosClimat'+iModel[1]+i+'.nc')
        #the piControl
        tsDs = fh.loadModelData(iModel[1], 'tos_Omon', 'piControl', iModel[2]).tos
        controlDs=tsDs.assign_attrs({'project_id':'CMIP'})
        
        pslClimat=xarray.open_dataset('results/cmipMonthlyIndeces/pslClimat'+iModel[1]+'.nc')
        pslControlDs=fh.loadModelData(iModel[1], 'psl_Amon', 'piControl', iModel[2])
        
        monthlyIndeces=allIndexCalc(controlDs,sstClimat,pslControlDs,pslClimat)
        monthlyIndeces.to_netcdf('results/cmipMonthlyIndeces/'+iModel[1]+'tospiControl.nc')
        
        indeces = tp.averageForTimePeriod(monthlyIndeces)
        
        indeces.assign_attrs(climatology='full length of pi Control')
        print('Caclulating control ...')
        indeces.to_netcdf(
            'results/cmipSeasonIndeces/'+iModel[1]+'tospiControl.nc')
        
    except Exception as e:
        print(iModel[1] + "piControl did not calculate")
        print(e) 

# Historical Indeces
for iModel in modelSet:
    
    print(iModel)
    
    try:    

        sstClimat=dict()

        for i in sstIndeces:
            sstClimat[i]=xarray.open_dataarray('results/cmipMonthlyIndeces/sstTosClimat'+iModel[1]+i+'.nc')
        pslClimat=xarray.open_dataset('results/cmipMonthlyIndeces/pslClimat'+iModel[1]+'.nc')

        #historical
        tsDs = fh.loadModelData(iModel[1], 'tos_Omon', 'historical', iModel[3]).tos
        sstDs=tsDs.assign_attrs({'project_id':'CMIP'})
        pslDs = fh.loadModelData(iModel[1], 'psl_Amon', 'historical',iModel[3])

        indeces = allIndexCalc(sstDs,sstClimat,pslDs,pslClimat)
        indeces.assign_attrs(climatology='full length of pi Control')
        
        #print(indeces)
        print('Caclulating historical ...')

        #save the results to file
        indeces.to_netcdf('results/cmipMonthlyIndeces/'+iModel[1]+'toshistorical.nc')
        
        
        indeces=xarray.open_dataset('results/cmipMonthlyIndeces/'+iModel[1]+'toshistorical.nc')
        
        tp.averageForTimePeriod(indeces).to_netcdf('results/cmipSeasonIndeces/'+iModel[1]+'toshistorical.nc')

    except Exception as e:
        print(iModel[1] + "historical did not calculate")
        print(e)
        


# Scenario Indeces
for iModel in modelSet:
    
    print(iModel)
    
    try: 

#ref to the saved files
        historicalIndeces = xarray.open_dataset('results/cmipMonthlyIndeces/'+iModel[1]+'toshistorical.nc' ,chunks='auto')
        
        sstClimat=dict()
        
        for i in sstIndeces:
            sstClimat[i]=xarray.open_dataarray('results/cmipMonthlyIndeces/sstTosClimat'+iModel[1]+i+'.nc',chunks='auto')
        pslClimat=xarray.open_dataset('results/cmipMonthlyIndeces/pslClimat'+iModel[1]+'.nc',chunks='auto')
        
        for experiment in scenarioSet: 
            try:
                variant = iModel[3]
                
                sstDs = fh.loadModelData(iModel[1], 'tos_Omon', experiment, variant).tos
                sstDs=sstDs.assign_attrs({'project_id':'CMIP'})

                pslDs = fh.loadModelData(iModel[1], 'psl_Amon', experiment,variant).psl.to_dataset()
                pslDs=pslDs.assign_attrs({'mip_era':'CMIP6'})

                indeces = xarray.concat([
                    historicalIndeces, 
                    allIndexCalc(sstDs,sstClimat,pslDs,pslClimat)
                ], 'time')

                indeces.assign_attrs(climatology='full length of pi Control')
                indeces.to_netcdf(
                    'results/cmipMonthlyIndeces/'+iModel[1]+'tos'+experiment+'.nc'
                )
                #print(indeces)
                print('Caclulating warm season avs and Writing to disk')
                
                answer=tp.averageForTimePeriod(indeces)
                
                answer.to_netcdf(
                    'results/cmipSeasonIndeces/'+iModel[1]+'tos'+experiment+'.nc'
                )

            except Exception as e:
                print(iModel[1] + experiment + " not completed: ")
                print(e)
                
            else:
                print(iModel[1] + experiment + ' complete')  

    except Exception as e:
        print(e)
        
    else:
        print(iModel[1] + ' finished')
