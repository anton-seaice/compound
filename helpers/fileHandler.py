#This is multi-dimensional array handling
import xarray

#This is file handling
from os import listdir


#Import regex 
import re

#This is to figure out which computer this is running on 
from platform import system

def getFilePaths(directory, filterTerm):
	# Directory to look for files
	operatingSystem = system()
	if operatingSystem == 'Windows':
    		directory = 'E:/CMIP5-PMIP3/CESM-LME/mon/SST/'
	elif operatingSystem == 'Darwin':
    		directory = '/Volumes/Untitled/CMIP5-PMIP3/CESM-LME/mon/SST/'
	else:
    		raise EnvironmentError("Can't find data files. Operating System is " + operatingSystem)
    

	# Get all the files in the directory
	fileList = listdir(directory)

	# Get ensemble run of interest
	regex = re.compile('b.e11.BLMTRC5CN.f19_g16.001.pop.h.SST.*.nc')
	listRun1 = list(filter(regex.match, fileList))

	listRun1 = [directory + f for f in listRun1]

	return listRun1

