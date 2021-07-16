import numpy

#cesm here referes to CESM LME

cesmFullForcings = ['001','002','003','004','005','006','007','008','009','010','011','012','013']

cesmCntl = '0850cntl.001'

cesmRcp85 = ['LME.002', 'LME.003', 'LME.008', 'LME.009']

cesmAll = [*cesmRcp85, cesmCntl, *cesmFullForcings]

cesmNoRepeats = [*cesmRcp85, '001','004','005','006','007','010','011','012','013']

#cmip6
deckSet=['piControl']#,'historical']
scenarioSet=['historical','ssp126', 'ssp245', 'ssp370','ssp585']
experimentSet=[*deckSet, *scenarioSet]
scenarioMip=numpy.array([ #Institution, Model, deckSetVariant, scenarioVariant
    ['CSIRO-ARCCSS', 'ACCESS-CM2', 'r1i1p1f1_gn', 'r1i1p1f1_gn'],
    ['CSIRO', 'ACCESS-ESM1-5', 'r1i1p1f1_gn', 'r1i1p1f1_gn'],
    ['BCC', 'BCC-CSM2-MR', 'r1i1p1f1', 'r1i1p1f1'],
    ['CAMS', 'CAMS-CSM1-0', 'r1i1p1f1', 'r1i1p1f1'],
    ['CAS', 'CAS-ESM2-0', 'r1i1p1f1', 'r1i1p1f1'],
    ['NCAR', 'CESM2', 'r3i1p1f1', 'r4i1p1f1'],
    ['NCAR', 'CESM2-WACCM', 'r1i1p1f1', 'r1i1p1f1'],
    ['THU', 'CIESM', 'r1i1p1f1', 'r1i1p1f1'],
    ['CMCC', 'CMCC-CM2-SR5', 'r1i1p1f1', 'r1i1p1f1'],
    ['CMCC', 'CMCC-ESM2', 'r1i1p1f1', 'r1i1p1f1'],
    ['CNRM-CERFACS', 'CNRM-CM6-1', 'r1i1p1f2', 'r1i1p1f2'],
    ['CNRM-CERFACS', 'CNRM-ESM2-1', 'r1i1p1f2', 'r1i1p1f2'],
    ['CCCma', 'CanESM5', 'r1i1p1f1', 'r1i1p1f1'],
    ['CCCma', 'CanESM5-CanOE', 'r1i1p2f1', 'r1i1p2f1'],
    ['EC-Earth-Consortium', 'EC-Earth3', 'r1i1p1f1', 'r1i1p1f1'],
    ['EC-Earth-Consortium', 'EC-Earth3-CC', 'r1i1p1f1', 'r1i1p1f1'],
    ['EC-Earth-Consortium', 'EC-Earth3-Veg', 'r1i1p1f1', 'r1i1p1f1'],
    ['EC-Earth-Consortium', 'EC-Earth3-Veg-LR', 'r1i1p1f1', 'r1i1p1f1'],
    ['FIO-QLNM','FIO-ESM-2-0','r1i1p1f1','r1i1p1f1'],
    ['NOAA-GFDL', 'GFDL-CM4', 'r1i1p1f1', 'r1i1p1f1'],
    ['NOAA-GFDL', 'GFDL-ESM4', 'r1i1p1f1', 'r1i1p1f1'],
    ['NASA-GISS', 'GISS-E2-1-G', 'r1i1p1f2', 'r1i1p1f2'],
    ['MOHC', 'HadGEM3-GC31-LL', 'r1i1p1f1', 'r1i1p1f3'], #NB the piControl used a slightly older version of the forcings.
    ['MOHC', 'HadGEM3-GC31-MM', 'r1i1p1f1', 'r1i1p1f3'],
    ['INM', 'INM-CM4-8', 'r1i1p1f1', 'r1i1p1f1'],
    ['INM', 'INM-CM5-0', 'r1i1p1f1', 'r1i1p1f1'],
    ['IPSL', 'IPSL-CM6A-LR', 'r1i1p1f1', 'r1i1p1f1'],
    ['NIMS-KMA', 'KACE-1-0-G', 'r1i1p1f1', 'r2i1p1f1'],
    ['UA', 'MCM-UA-1-0', 'r1i1p1f1', 'r1i1p1f2'],
    ['MIROC', 'MIROC-ES2L', 'r1i1p1f2_gn', 'r1i1p1f2_gn'],
    ['MIROC', 'MIROC6', 'r1i1p1f1', 'r1i1p1f1'],
    ['MPI-M', 'MPI-ESM1-2-HR', 'r1i1p1f1', 'r1i1p1f1'],
    ['MPI-M', 'MPI-ESM1-2-LR', 'r1i1p1f1', 'r1i1p1f1'],
    ['MRI', 'MRI-ESM2-0', 'r1i1p1f1_gn', 'r1i1p1f1_gn'],
    ['NUIST', 'NESM3', 'r1i1p1f1', 'r1i1p1f1'],
    ['NCC', 'NorESM2-LM', 'r1i1p1f1', 'r1i1p1f1'],
    ['NCC', 'NorESM2-MM', 'r1i1p1f1', 'r1i1p1f1'],
    ['MOHC', 'UKESM1-0-LL', 'r1i1p1f2', 'r1i1p1f2']
])

##no SSP 585
    #['EC-Earth-Consortium', 'EC-Earth3-AerChem', 'r1i1p1f1', 'r1i1p1f1'],
    #['IPSL', 'IPSL-CM5A2-INCA', 'r1i1p1f1', 'r1i1p1f1'],
    #['HAMMOZ-Consortium', 'MPI-ESM-1-2-HAM', 'r1i1p1f1', 'r1i1p1f1'],

    #piControl < 500 years
    #['E3SM-Project', 'E3SM-1-1', 'r1i1p1f1', 'r1i1p1f1'],
    #['CCCR-IITM', 'IITM-ESM', 'r1i1p1f1', 'r1i1p1f1'],
    #['CNRM-CERFACS', 'CNRM-CM6-1-HR', 'r1i1p1f2', 'r1i1p1f2'],
    
    #no Pr!
    #['FIO-QLNM', 'FIO-ESM-2-0', 'r1i1p1f1', 'r1i1p1f1'],
    #['KIOST', 'KIOST-ESM', 'r1i1p1f1', 'r1i1p1f1'],
    
    #cutting this because its badly formatted
    #['AWI', 'AWI-CM-1-1-MR', 'r1i1p1f1', 'r1i1p1f1'],
    
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