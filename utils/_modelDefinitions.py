#cesm here referes to CESM LME

cesmFullForcings = ['001','002','003','004','005','006','007','008','009','010','011','012','013']

cesmCntl = ['0850cntl.001']

cesmRcp85 = ['LME.002', 'LME.003', 'LME.008', 'LME.009']

cesmAll = [*cesmRcp85, *cesmCntl, *cesmFullForcings]

#cmip

past1000 = [
    'bcc-csm1-1',
    #'CCSM4',
    'CSIRO-Mk3L-1-2',
    'FGOALS-gl',
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