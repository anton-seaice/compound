#!/usr/bin/env python3
# coding: utf-8

# # cmip Temp and Rainfall Anomalies

#import my functions
import helpers.fileHandler as fh
import utils._modelDefinitions as _model
import utils._indexDefinitions as _index
import utils.timePeriod as tp

import xarray
import numpy
import cftime
import xesmf as xe #this is the regrid package

#turn off warnings
import warnings
warnings.filterwarnings('ignore')


#the data is in kg/(m2 s), to convert to mm/day:
secondsPerDay = 60*60*24
secondsToTimeP = secondsPerDay #seconds per day, convert m to mm

#the lon/lat grid we are going to use for all models
regridXr=xarray.Dataset({'lat': (['lat'], numpy.arange(-50, 0, 1.5)),
                     'lon': (['lon'], numpy.arange(100, 170, 1.5)),
                    }
                   )


for model in _model.scenarioMip:
    #Calculate a climatology
    #Based on the control run, calculate monthly anomalies
    
    try:
        print(model)
        xr = xarray.merge([
            fh.loadModelData(model[1], 'pr_Amon', 'piControl', model[2]).pr*secondsToTimeP,
            fh.loadModelData(model[1], 'tas_Amon', 'piControl', model[2]).tas
        ], compat='override')

        domainXr=xr.where(
                (xr.lat>-50) & (xr.lat<0) & (xr.lon>100) & (xr.lon<170),
                drop=True
            )

        #regrid before processing
        regridder = xe.Regridder(domainXr, regridXr, 'bilinear')
        newXr=regridder(domainXr)

        monMeansDa=newXr.groupby('time.month').mean(dim='time')
        monMeansDa.to_netcdf('results/cmipMonthlyPrTs/monMeans'+model[1]+'.nc')

        monMeansDa=xarray.open_dataset(
            'results/cmipMonthlyPrTs/monMeans'+model[1]+'.nc')

        #anom for piControl
        anomDa=newXr.groupby('time.month')-monMeansDa
        
        #warmSeasonAv
        warmSeasonAnomDa=tp.averageForTimePeriod(anomDa.rename({'tas':'ts'}))
        warmSeasonAnomDa['model']=model[1]
        warmSeasonAnomDa = warmSeasonAnomDa.assign_attrs([*warmSeasonAnomDa.attrs, ('units','mm/month'), ('timePeriod','Warm Season')])
        
        warmSeasonAnomDa.to_netcdf(
            'results/cmipSeasonPrTs/'+model[1]+'PiControl.nc')
    
    
    except Exception as e:
        print(e)
    
    #calculate anomalies for all scenarios
        for experiment in ['ssp585']:

            try: 
                #load it
                monMeansDa=xarray.open_dataset(
                'results/cmipMonthlyPrTs/monMeans'+model[1]+'.nc')

                xr = xarray.merge(
                    [
                        xarray.concat(
                            [
                                fh.loadModelData(model[1], 'pr_Amon', 'historical', model[3]), 
                                fh.loadModelData(model[1], 'pr_Amon', experiment, model[3])
                            ],
                        'time').pr*secondsToTimeP,
                        xarray.concat(
                            [
                                fh.loadModelData(model[1], 'tas_Amon', 'historical', model[3]),
                                fh.loadModelData(model[1], 'tas_Amon', experiment, model[3])
                            ],
                        'time').tas
                ], compat='override')

                        #grab area around Australia
                domainXr=xr.where(
                    (xr.lat>-50) & (xr.lat<0) & (xr.lon>100) & (xr.lon<170),
                    drop=True
                )

                #regrid before processing
                regridder = xe.Regridder(domainXr, regridXr, 'bilinear')
                newXr=regridder(domainXr)

                anomDa=newXr.groupby('time.month')-monMeansDa
                
                #warmSeasonAv
                warmSeasonAnomDa=tp.averageForTimePeriod(anomDa.rename({'tas':'ts'}))
                warmSeasonAnomDa['model']=model[1]
                warmSeasonAnomDa = warmSeasonAnomDa.assign_attrs([*warmSeasonAnomDa.attrs, ('units','mm/month'), ('timePeriod','Warm Season')])

                warmSeasonAnomDa.to_netcdf(
                    'results/cmipSeasonPrTs/'+model[1]+experiment+'.nc')

            except Exception as e:
                print(model[1] + experiment + " did not calculate")
                print(e)


