import re #regex

#python number and array handling
import cftime
import pandas
import numpy
import xarray

# Import my functions
from sys import path
path.append('../')
import helpers.cvdpTime as cvdpTime
import utils._modelDefinitions as _model
import helpers.esgfClient as esgfClient
from helpers.basePath import basePath

from platform import node


def institutionFinder(model) :
    """ Find the instituion for this model and return it"""
    for i in numpy.arange(0, len(_model.scenarioMip)):
        if model==_model.scenarioMip[i,1]:
            return _model.scenarioMip[i,0]
    raise EnvironmentError("Institution not found for this model")

def to_365day_monthly(da):
    '''Takes a DataArray. Change the calendar to 365_day and precision to monthly.'''
    val = da.copy()
    time1 = da.time.copy()
    for itime in range(val.sizes['time']):
        bb = val.time.values[itime].timetuple()
        time1.values[itime] = cftime.DatetimeNoLeap(bb[0],bb[1],16)
    val = val.assign_coords({'time':time1})
    return val

        
def getFilePaths(directory, *args):
    """Returns a list of absolute paths from a chosen directory
    
    Chosen directory is relative to the CMIP5-PMIP3 folder (i.e. where all models are kept)
    
    Optionally a second argument can be a regex term to search the chosen directory (default is all .nc files in the directory)
    
    This is set-up for the developers environment
    
    """
    
    from os import listdir
    # First, see if there is a second argument. If there is then this is the filterTerm, otherwise its just all .nc files
    if len(args)==0:
        filterTerm = '.+\.nc'
    elif len(args)==1:
        filterTerm = args[0]
    else:
        raise EnvironmentError("Wrong number of arguments provided")
    
    # Second, find a path to look for files
    directory = basePath() + directory
    
    # Get all the files in the directory
    try:
        fileList = listdir(directory)
    except:
        raise EnvironmentError("Requested files " + directory + " not found. Is the harddrive plugged in?")
    
    # Get list of files from model run of interest accoding to the filter term
    regex = re.compile(filterTerm)
    listRun1 = list(filter(regex.match, fileList))
    listRun1 = [directory + f for f in listRun1]

    return listRun1

def constructDirectoryPath(model, outputType, *args):
    """Creates a directory name from arguments provided
    
    valid inputs are: 
    model: 'CESM-LME'. 'CMIP6'
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
        if outputType == 'CVDP':
            directory = 'cmip6.'+ args[0] +'.cvdp_data/'
        elif node().split('-')[0]=='gadi':
            if any([model=='piControl', model=='historical']):
                directory = 'CMIP6/CMIP/'
            else:
                directory = 'CMIP6/ScenarioMIP/'
        else:
            directory = 'CMIP6/'
       
    return directory

def loadModelData(model, variable, test,*args, **kargs):
    """Opens data for the chosen model (CESM-LME is supported and CMIP6)
    
    model = 'CESM-LME, past1000, historical, pi-control'
    variable = folder name for that variable, or 'cvdp_data' if desired
    test = name of model run, e.g. '001', or 'ORBITAL.003'
    
    """
    import subprocess
    
    
    #make a regex to compare the variable name against, as cvdp is a special case.
    cvdpRegex=re.compile('cvdp')
    
    #args might be a variant for CMIP6
    if len(args)==1:
        variant=args[0]
    else:
        variant='r1i1p1f1' #used for CMIP6 only
    
#First we are going to make some file paths from the information provided.
    #CESM-LME
    if model=='CESM-LME' :
        #for CESM, make a filter term for file names, and make a directory
        #exampleFilterTerm = 'b\.e11\.BLMTRC5CN\.f19_g16.001\.pop\.h\.SST\..+\.nc'
        filterTerm = 'b\.e11\.B.*?\.f19_g16\.' + test + '\..*?' + variable + '\..+\.nc'
         
        if cvdpRegex.search(variable):
            #for cvdp, special case
            directory = constructDirectoryPath('CESM-LME', 'CVDP')
        else :
            #for normal experiments
            directory = constructDirectoryPath('CESM-LME', 'MON', variable)
    
    #CVDP for other models (CMIP)
    elif cvdpRegex.search(variable):
        filterTerm = model+'_'+variant+'\.cvdp_data\..*\.nc'
        directory = constructDirectoryPath(model, 'CVDP', test)
    
    #other cmip5
    #elif test=='past1000' or test=='historical' or test=='piControl':
    else:
        filterTerm = variable + '_.*?'+model+'_'+test+'_'+variant+'_.*'#'?\.nc' # if CMIP table not specified, its assumed from .+?
        directory = constructDirectoryPath(test, 'MON', variable)

#Second get an list of paths for that filer term and directory  

    print(basePath()+directory)
    print(filterTerm)
    if node().split('-')[0]=='gadi':
        find=(subprocess.run(['find',
                              basePath()+directory+'/'+institutionFinder(model)+'/'+model+'/'+test+'/'+variant,
                              '-regex',
                              '.*\\'+filterTerm] , capture_output=True).stdout)
        paths=find.decode("utf-8").split('\n')[:-1]
    else:
        paths = getFilePaths(directory, filterTerm)
        #if nothing try online from esgf
        if len(paths)==0:
            esgfClient.esgfDownloader(model, variable, test, variant)
            paths = getFilePaths(directory, filterTerm)
    
    # throw an error if we still didn't find any files      
    if len(paths)==0:
        raise EnvironmentError("Files (filter term: " + filterTerm + " ) not found, possibly test name is wrong")

    print(paths)
        
#Third, open the Xr
    if cvdpRegex.search(variable):
        #special case for cvdp, as the times are really weird
        result = xarray.open_mfdataset(paths, decode_times=False, **kargs)
        result = cvdpTime.decodeTime(result)
    elif model == 'CESM-LME':
            #special case for CESM, as the dates are one day later then you expect. (i.e. the average for the first month of 850 is associated with the time co-ord of 1-Feb-850)
            result = xarray.open_mfdataset(paths, **kargs)
            result['time'] = result['time']-pandas.to_timedelta(1, unit='d')
    else:
        # other model types.
        result = xarray.open_mfdataset(paths, use_cftime=True, **kargs)

        #If there is a time coord, then make it monthly using 365 cal
        timeRe=re.compile('time')
        cfTimeRe=re.compile('cftime._cftime.DatetimeNoLeap')
        for i in list(result.coords) :
            if timeRe.search(i) :
                #if not(cfTimeRe.search(str(type(result.time.values[0])))):
                    result = to_365day_monthly(result)
                    
    #Fourth - make some dumb corrections
    #most model use 'lon' and 'lat', so use these if they have used 'longitude' and 'latitude'
    latRe=re.compile('latitude')
    matches = [latRe.search(string) for string in list(result.coords)]
    for m in matches:
        if m!=None:
             if m.span()==(0,8): #this is a weid way of matching?
                    result=result.rename({'latitude':'lat', 
                                'longitude':'lon'})
    #standardise all models to use 0 to 360E (instead of -180 to 180)                
    #result['lon']=(result.lon.where(result.lon<0)+360)

    
    return result




    
