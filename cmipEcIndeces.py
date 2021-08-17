#!/usr/bin/env python3
# coding: utf-8

import sys
sys.path.append(sys.path[0]+'/../')

# handy python functions
import xarray

#import my functions
import helpers.fileHandler as fh
import utils._modelDefinitions as _model
import utils.ecIndex as ec

# turn off warnings:
import warnings
warnings.filterwarnings('ignore')

#the full model set
modelSet=_model.scenarioMip

# For all the models, calculate the alphas and e/c Index

for iModel in modelSet:
    try:
        print(iModel[1])
        
        #Load the ssts from piControl
        climatXr=fh.loadModelData(iModel[1], 'tos_Omon', 'piControl', iModel[2]).tos
        climatXr=climatXr.assign_attrs({'project_id':'CMIP'})
                
        tsXr=climatXr
        
        #Calculate anomalies using piControl baseline
        sstAnomXr=ec.sstAnoms(tsXr, climatXr)
        
        #create the solver
        solver=ec.eofSolver(sstAnomXr)
        
        #caluculate pcs and eofs
        indeces, pFit, eofsXr = ec.pcs(solver)
                
        eofsXr.to_netcdf('results/cmipEcIndex/eof'+str(iModel[1])+'.nc')
        indeces.to_netcdf('results/cmipEcIndex/pcPiControl'+str(iModel[1])+'.nc')
    except Exception as e:
        print(e)
    
    for iExp in [#'ssp126', 'ssp245', 'ssp370',
        'ssp585']:#load the ssts from ssp585
        try:
            tsXr = xarray.concat(
                [
                    fh.loadModelData(iModel[1], 'tos_Omon', 'historical', iModel[3]).tos, 
                    fh.loadModelData(iModel[1], 'tos_Omon', iExp, iModel[3]).tos
                ], 
                dim='time')
            tsXr=tsXr.assign_attrs({'project_id':'CMIP'})

            #Calculate anomalies using piControl baseline
            sstAnomXr=ec.sstAnoms(tsXr, climatXr)

            #project these anomalies onto the Eofs from piControl
            expPcs=solver.projectField(sstAnomXr)

            #reformat for consistency
            indeces = xarray.merge([expPcs.sel(mode=0, drop=True).rename('pc1'),
                                expPcs.sel(mode=1, drop=True).rename('pc2'), 
                               ])

            indeces.to_netcdf('results/cmipEcIndex/pc'+iExp+str(iModel[1])+'.nc')
        
        
        except Exception as e:
            print(e)
