#This is multi-dimensional array handling
import xarray

#This is file handling
from os import listdir

#Import regex 
import re

#This is to figure out which computer this is running on 
from platform import system

#Import logging
import logging

# Import cvdp time function
import sys
sys.path.append('../')
import helpers.cvdpTime as cvdpTime

import pandas

def getFilePaths(directory, *args):
    """Returns a list of absolute paths from a chosen directory
    
    Chosen directory is relative to the CMIP5-PMIP3 folder (i.e. where all models are kept)
    
    Optionally a second argument can be a regex term to search the chosen directory (default is all .nc files in the directory)
    
    """
    # First, see if there is a second argument. If there is then this is the filterTerm, otherwise its just all .nc files
    if len(args)==0:
        filterTerm = '.+\.nc'
    elif len(args)==1:
        filterTerm = args[0]
    else:
        raise EnvironmentError("Wrong number of arguments provided")
    
    # Second, find a path to look for files
    operatingSystem = system()
    if operatingSystem == 'Windows':
        directory = 'E:/CMIP5-PMIP3/' + directory
    elif operatingSystem == 'Darwin':
        directory = '/Volumes/Untitled/CMIP5-PMIP3/'  + directory 
    else:
        raise EnvironmentError("Can't find where to look for data files. Operating System is " + operatingSystem)
    

    # Get all the files in the directory
    try:
        fileList = listdir(directory)
    except:
        raise EnvironmentError("Requested files not found. Is the harddrive plugged in and does this test case exist?")
    
    # Get list of files from model run of interest accoding to the filter term
    regex = re.compile(filterTerm)
    listRun1 = list(filter(regex.match, fileList))
    listRun1 = [directory + f for f in listRun1]

    return listRun1



def constructDirectoryPath(model, outputType, *args):
    """Creates a directory name from arguments provided
    
    
    valid inputs are: 
    model: 'CESM-LME'
    outputType: 'CVDP', 'DAY', 'MON'
    *args: This is the variable desired
    
    Note there is no range checking on the last argument (should be a valid output variable for the desired model output)."""
    # First, see if there is a third argument. If there is then this is the filterTerm, otherwise its just all .nc files
    if outputType not in ('CVDP','DAY','MON'):
        raise EnvironmentError(outputType + ' is not a valid type')
    
    if outputType in ('DAY','MON'):
        if len(args)!=1:
            raise EnvironmentError("Wrong number of arguments provided")
    
    if model == 'CESM-LME':
        if outputType == 'CVDP':
            directory = 'CESM-LME/cesm1.lm.cvdp_data/'
        elif outputType == 'DAY':
            directory = 'CESM-LME/day/' + args[0] + '/'
        elif outputType == 'MON':
            directory = 'CESM-LME/mon/' + args[0] + '/'
    else:
        raise EnvironmentError("Selected model not found")
    
    return directory

def loadModelData(model, variable, test, **openDatasetKwargs):
    """Loads data for the chosen model (CESM-LME is supported)
    
    
    model = 'CESM-LME'
    variable = folder name for that variable, or 'cvdp_data' if desired
    test = name of model run, e.g. '001', or 'ORBITAL.003'
    keyword arguments are passted to the Xarray mfopen dataset (most likely to use decode_times=False, otherwise look at open_mfdataset documentation)
    
    
    """
    
    #First we are going to make some file paths from the information provided.
    
    #make a regex to compare the variable name against, as cvdp is a special case.
    regex=re.compile('cvdp')
    
    if model=='CESM-LME' :
        #for CESM, make a filter term for file names, and make a directory
        #exampleFilterTerm = 'b\.e11\.BLMTRC5CN\.f19_g16.001\.pop\.h\.SST\..+\.nc'
        filterTerm = 'b\.e11\.B.*?\.f19_g16\.' + test + '\..*?' + variable + '\..+\.nc'
         
        if regex.search(variable):
            #for cvdp, special case
            directory = constructDirectoryPath('CESM-LME', 'CVDP')
        else :
            #for normal experiments
            directory = constructDirectoryPath('CESM-LME', 'MON', variable)
    else:
        #otherwise we are just going to throw an error
        raise EnvironmentError("Selected model not supported, please add to file handler")  

    print(directory)
    print(filterTerm)
    #get an array of paths for that filer term and directory    
    paths = getFilePaths(directory, filterTerm)
    
    print(paths)
    print(len(paths))
    print(len(paths)==0)
    # throw an error if we didn't find any files
    if len(paths)==0:
        raise EnvironmentError("Files not found, possibly test name is wrong")
    
    print(paths)
    #At some point, it could be interesting to write this without dask. To do this you would open each file individually and then cat them. (Possible it would make sense to reduce their size first to)
    

    if model == 'CESM-LME':
        if regex.search(variable):
            #special case for cvdp, as the times are really weird
            result = xarray.open_mfdataset(paths, decode_times=False, **openDatasetKwargs)
            result = cvdpTime.decodeTime(result)
        else:
            #special case for CESM, as the dates are one day later then you expect. (i.e. the average for the first month of 850 is associated with the time co-ord of 1-Feb-850)
            result = xarray.open_mfdataset(paths, **openDatasetKwargs)
            result['time'] = result['time']-pandas.to_timedelta(1, unit='d')
    else:
        # basically a place holder for other model types.
        result = xarray.open_mfdataset(paths, **openDatasetKwargs)
    
    print("Files imported: \n",paths)
    
    return result
