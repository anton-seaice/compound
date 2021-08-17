import numpy

#cesm here referes to CESM LME
cesmFullForcings = ['001','002','003','004','005','006','007','008','009','010','011','012','013']
cesmCntl = '0850cntl.001'
cesmRcp85 = ['LME.002', 'LME.003', 'LME.008', 'LME.009']
cesmAll = [*cesmRcp85, cesmCntl, *cesmFullForcings]
cesmNoRepeats = [*cesmRcp85, '001','004','005','006','007','010','011','012','013']





#cmip6
deckSet=['piControl']#,'historical']
scenarioSet=[#'historical','ssp126', 'ssp245', 'ssp370',
    'ssp585']
experimentSet=[*deckSet, *scenarioSet]
scenarioMip=numpy.array([ #Institution, Model, deckSetVariant, scenarioVariant
    ['CSIRO-ARCCSS', 'ACCESS-CM2', 'r1i1p1f1_gn', 'r1i1p1f1_gn'],
    ['CSIRO', 'ACCESS-ESM1-5', 'r1i1p1f1_gn', 'r1i1p1f1_gn'],
    ['AWI', 'AWI-CM-1-1-MR', 'r1i1p1f1', 'r1i1p1f1'],
    ['BCC', 'BCC-CSM2-MR', 'r1i1p1f1', 'r1i1p1f1'],
    ['CAMS', 'CAMS-CSM1-0', 'r1i1p1f1', 'r1i1p1f1'],
    ['CAS', 'CAS-ESM2-0', 'r1i1p1f1', 'r1i1p1f1'],
    ['NCAR', 'CESM2', 'r1i1p1f1', 'r4i1p1f1'],
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
    
    # no Tos (no ocean?)
    #['NIMS-KMA', 'KACE-1-0-G', 'r1i1p1f1', 'r2i1p1f1'],

    
wangsAnswers={'CAMS-CSM1-0':-0.2902, 
    'CMCC-CM2-SR5':-0.4055, 
    'CNRM-CM6-1':-0.1662, 
    'CNRM-ESM2-1':-0.1687,
    'EC-Earth3':-0.2662, 
    'EC-Earth3-Veg':-0.2665, 
    #'FIO-ESM-2-0':-0.3751,
    'MIROC6':-0.3198, 
    'MIROC-ES2L': -0.3466,
    'HadGEM3-GC31-LL':-0.1785, 
    'MPI-ESM1-2-HR':-0.2660, 
    'MPI-ESM1-2-LR':-0.2338, 
    'MRI-ESM2-0':-0.3387,
    'GISS-E2-1-G':-0.3644, 
    'CESM2':-0.3216, 
    'CESM2-WACCM':-0.2436, 
    'NorESM2-LM':-0.2505, 
    'NorESM2-MM':-.2077,
    #'GFDL-ESM4':-.1931, 
    'CIESM':-.1886, 
    'MCM-UA-1-0':-0.2888}

wangModelSet = list(wangsAnswers.keys())
