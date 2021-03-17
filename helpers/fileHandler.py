#This is multi-dimensional array handling
import xarray

#This is file handling
from os import listdir

#Import regex 
import re

#This is to figure out which computer this is running on 
from platform import system


def getFilePaths(directory, *args):
    """Returns a list of absolute paths from a chosen directory and file name filter
    
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
        directory = '/Volumes/Untitled/'  + directory +'/'
    else:
        raise EnvironmentError("Can't find where to look for data files. Operating System is " + operatingSystem)
    

    # Get all the files in the directory
    fileList = listdir(directory)

    # Get list of files from model run of interest accoding to the filter term
    regex = re.compile(filterTerm)
    listRun1 = list(filter(regex.match, fileList))
    listRun1 = [directory + f for f in listRun1]

    return listRun1

