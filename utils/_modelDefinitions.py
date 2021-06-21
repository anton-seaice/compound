import numpy

#cesm here referes to CESM LME

cesmFullForcings = ['001','002','003','004','005','006','007','008','009','010','011','012','013']

cesmCntl = '0850cntl.001'

cesmRcp85 = ['LME.002', 'LME.003', 'LME.008', 'LME.009']

cesmAll = [*cesmRcp85, cesmCntl, *cesmFullForcings]

cesmNoRepeats = [*cesmRcp85, '001','004','005','006','007','010','011','012','013']

#cmip6

scenarioMIP=modelSet=numpy.array([
    #['CSIRO-ARCCSS', 'ACCESS-CM2'],
    #['CSIRO', 'ACCESS-ESM1-5'],
    ['AWI', 'AWI-CM-1-1-MR'],
    #['BCC', 'BCC-CSM2-MR'],
    ['CAMS', 'CAMS-CSM1-0'],
    ['CAS', 'CAS-ESM2-0'],
    ['NCAR', 'CESM2'],
    ['NCAR', 'CESM2-WACCM'],
    ['THU', 'CIESM'],
    ['CMCC', 'CMCC-CM2-SR5'],
    ['CMCC', 'CMCC-ESM2'],
    ['CNRM-CERFACS', 'CNRM-CM6-1'],
    ['CNRM-CERFACS', 'CNRM-CM6-1-HR'],
    ['CNRM-CERFACS', 'CNRM-ESM2-1'],
    ['CCCma', 'CanESM5'],
    ['CCCma', 'CanESM5-CanOE'],
    ['E3SM-Project', 'E3SM-1-1'],
    ['EC-Earth-Consortium', 'EC-Earth3'],
    ['EC-Earth-Consortium', 'EC-Earth3-AerChem'],
    ['EC-Earth-Consortium', 'EC-Earth3-CC'],
    ['EC-Earth-Consortium', 'EC-Earth3-Veg'],
    ['EC-Earth-Consortium', 'EC-Earth3-Veg-LR'],
    ['FIO-QLNM', 'FIO-ESM-2-0'],
    ['NOAA-GFDL', 'GFDL-CM4'],
    ['NOAA-GFDL', 'GFDL-ESM4'],
    ['NASA-GISS', 'GISS-E2-1-G'],
    ['MOHC', 'HadGEM3-GC31-LL'],
    ['MOHC', 'HadGEM3-GC31-MM'],
    ['CCCR-IITM', 'IITM-ESM'],
    ['INM', 'INM-CM4-8'],
    ['INM', 'INM-CM5-0'],
    ['IPSL', 'IPSL-CM5A2-INCA'],
    ['IPSL', 'IPSL-CM6A-LR'],
    ['NIMS-KMA', 'KACE-1-0-G'],
    ['KIOST', 'KIOST-ESM'],
    ['UA', 'MCM-UA-1-0'],
    ['MIROC', 'MIROC-ES2L'],
    ['MIROC', 'MIROC6'],
    ['HAMMOZ-Consortium', 'MPI-ESM-1-2-HAM'],
    ['MPI-M', 'MPI-ESM1-2-HR'],
    ['MPI-M', 'MPI-ESM1-2-LR'],
    ['MRI', 'MRI-ESM2-0'],
    ['NUIST', 'NESM3'],
    ['NCC', 'NorESM2-LM'],
    ['NCC', 'NorESM2-MM'],
    ['MOHC', 'UKESM1-0-LL']
])

#cmip5

past1000 = [
    #'bcc-csm1-1',
    #'CCSM4',
    'CSIRO-Mk3L-1-2',
    #'FGOALS-gl',
    'FGOALS-s2',
    'GISS-E2-R',
    'HadCM3',
    'IPSL-CM5A-LR',
    'MIROC-ESM',
    'MPI-ESM-P',
    'MRI-CGCM3'
]

historical = [
    'ACCESS1-3',
    'bcc-csm1-1',
    'BNU-ESM',
    'CanCM4',
    'CanESM2',
    #'CCSM4', #Not sure if i should include?
    'CESM1-BGC',
    'CESM1-CAM5',
    'CMCC-CESM',
    'CMCC-CM',
    'CMCC-CMS',
    'CNRM-CM5',
    'CSIRO-Mk3-6-0',
    'CSIRO-Mk3L-1-2',
    'EC-EARTH',
    'FGOALS-g2',
    'FGOALS-s2',
    'FIO-ESM',
    'GFDL-CM2p1',
    'GFDL-CM3',
    'GFDL-ESM2G',
    'GFDL-ESM2M',
    'GISS-E2-H',
    'GISS-E2-R',
    'HadCM3',
    'HadGEM2-AO',
    'HadGEM2-CC',
    'HadGEM2-ES',
    'inmcm4',
    'IPSL-CM5A-LR',
    'IPSL-CM5A-MR',
    'IPSL-CM5B-LR',
    'MIROC5',
    'MIROC-ESM',
    'MPI-ESM-LR',
    'MPI-ESM-MR',
    'MPI-ESM-P',
    'MRI-CGCM3',
    'MRI-ESM1',
    'NorESM1-M',
    'NorESM1-ME'
]