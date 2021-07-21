#!/usr/bin/env python3
# coding: utf-8

# # Test CMIP6 Download

# 1. Confirm all four variables have been downloaded for all experiments
# 2. Confirm downloaded variables all cover the same time ranges for all experiments
# 3. Confirm calculated indices cover the same time range


import sys
sys.path.append(sys.path[0]+'/../')

#import my functions
import helpers.fileHandler as fh
import utils._modelDefinitions as _model

#normal xarray/plotting stuff

import xarray
import numpy
import matplotlib.pyplot as plt


#turn of warnings
import warnings
warnings.filterwarnings('ignore')

#turn on dask explicitly
#import climtas.nci
#client=climtas.nci.GadiClient()

# These are the experiments

deckSet=['piControl','historical']
scenarioSet=[#'ssp126', 'ssp245', 'ssp370',
    'ssp585']
experimentSet=[*deckSet, *scenarioSet]


# These are the models


modelSet=_model.scenarioMip



# for all models ....
for i in range(0,len(modelSet)):
  # everyone loves nested for loops  
    iModel=modelSet[i]
    print(str(i) + str(iModel))
    
    #for all experiments in that model ...
    for experiment in experimentSet: 
        
        #choose the right variant field
        if experiment=='piControl':
            variant = iModel[2]
        else:
            variant = iModel[3]

        try:
            #calculated indeces
            indecesDs = xarray.open_dataset(
                '../results/cmipWarmSeasonIndeces/' + iModel[1] +'tos'+ experiment + '.nc')

            calc=[indecesDs.year.values[0], #start year
                indecesDs.year.values[-1]+1] #end year
            
            #for all four variables
            for variable in ['ts_Amon', 'psl_Amon','pr_Amon', 'tas_Amon', 'tos_Omon']:
                
                try:
                    #open the files
                    sourceXr = fh.loadModelData(iModel[1], variable, experiment, variant)
                
                    #start year, end year for each experiment
                    if experiment=='piControl':
                        source=[sourceXr.time.dt.year.values[0],
                            sourceXr.time.dt.year.values[-1]]
                    elif experiment=='historical':
                        histStart=sourceXr.time.dt.year.values[0]
                        source=[histStart,
                            sourceXr.time.dt.year.values[-1]]
                    else:
                        #the remaining experiments are the scenarios,
                        #where indices start in the historical dataset 
                        #and move to the scenario part way through
                        source=[histStart,
                            sourceXr.time.dt.year.values[-1]]
                
                    #compare start year and end year for this variable to the indeces calculated
                    if not(numpy.array_equal(source,calc)):
                        print('noMatch' + experiment + variable)
                        print('calculated ... sourceFile')
                        print([*calc, *source])
           
                except Exception as e:
                    print(e)

            #check how long the piControl is
            #(should be 500 years per CMIP specs, 
            #but some models appear not to have recalculated for all variants)
            if all(
            [calc[1]-calc[0]<400, 
             experiment=='piControl']
            ):
                print('piControl too short')
                print([*calc, *source])
        
        
        except Exception as e:
            print(experiment + ':')
            print(e)
        
        


# Those errors all look ok:
# 
# 3: BCC - the source file has both a latitude and lat, so it gives this warning but is ok.
# 
# 5: Not really sure why times are different between the two, but there you go.
# 

# In[ ]:




