#!/usr/bin/env python3
# coding: utf-8

import sys
sys.path.append(sys.path[0]+'/../')

#import my functions
import helpers.fileHandler as fh
import utils._modelDefinitions as _model
import utils.ecIndex as ec

# handy python functions
import xarray

# turn off warnings:
import warnings
warnings.filterwarnings('ignore')

#the full model set
modelSet=[_model.scenarioMip[35]]

# For all the models, calculate the alphas and e/c Index

for iModel in modelSet:
    try:
        print(iModel[1])
        
        climatXr=fh.loadModelData(iModel[1], 'tos_Omon', 'piControl', iModel[2]).tos
        
        tsXr = xarray.concat([
            fh.loadModelData(iModel[1], 'tos_Omon', 'historical', iModel[3]).tos, 
            fh.loadModelData(iModel[1], 'tos_Omon', 'ssp585', iModel[3]).tos
        ], dim='time')
       
        sstAnomXr=ec.sstAnoms(tsXr, climatXr)

        indeces, pFit, eofsXr = ec.ecIndex(sstAnomXr)
                
        indeces.to_netcdf('results/ecIndex/index'+str(iModel[1])+'.nc')
        eofsXr.to_netcdf('results/ecIndex/eof'+str(iModel[1])+'.nc')
        
    except Exception as e:
        print(e)

