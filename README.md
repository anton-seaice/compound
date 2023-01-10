# compound

This is a collection of scripts to examine changing frequenices of compounding impacts from multiple climate drivers upon mainland south east Australia.

Developed using python 3.7

IDE versioning

jupyter core     : 4.7.1
jupyter-notebook : 6.3.0
qtconsole        : 5.0.3
ipython          : 7.22.0
ipykernel        : 5.3.4
jupyter client   : 6.1.12
jupyter lab      : 3.0.14
nbconvert        : 6.0.7
ipywidgets       : 7.6.3
nbformat         : 5.1.3
traitlets        : 5.0.5

Dependencies

xarray 0.18.0
numpy 1.17.0
cartopy 0.18.0
eofs [https://github.com/ajdawson/eofs/tree/9d206001a1d841fa649dce359554d43e315801b6]
nc-time-axis 1.3.1
xesmf 0.5.3
matplotlib 3.4.2


If you prefer, there is a yaml file in ref folder, or you can 
`module use /g/data/hh5/public/modules
module load conda/analysis3`
on nci. (With the exception of the eofs package)

CESM Descriptions:

1. cesmIndeces/cesmPrecTsMonthly
- Calculates monthly indeces (for indeces included in utils/_indexDefinitions.py)
- Calculates seasonal averages (time periods defined in utils/_indexDefinitions.py)
This will attempt to pull the CESM-LME results from an external harddrive, you would need to fix the paths if you re-run these.
The output from these files is saved in results/cesmTradIndeces.nc, results/cesmPrecAnoms.nc and results/cesmTsAnoms.nc

2. cesmCompounds
- Plots of annual trends in enso, iod, sam
- Example of how events compound to be fire promoting or not-fire promoting
- Plots of 30 year trends in compounding events

3. cesmCompoundsType
- Plots of 30 years trends in compounding events, seperated by event type (i.e. on of the three pairs or all3)

4. cesmCompoundImpacts
- Rainfall and Temp anomaly maps for each individial event type, and each compound event type ( I think this needs updating to show seperate cool season and warm season impacts).

CMIP6 Descriptuons

1. cmipIndeces.py, cmipEcIndeces.py and cmipPrTs.py
- Calulcates monthly indeces and seasonal averages
This will attempt the pull the CMIP results from gadi, for the models defined in utils/_modelDefinitions.py. These paths may well be broken / need updating. This uses helpers/fileHandler.py, which is very messy/needs a rewrite.
The output from these files is saved in results/cmipEcIndex/, results/cmipSeasonIndeces, cmipSeasonPrTs

2. cmipIndeces
- Plots of individual indeces, and looks at impact of detrending and comparisons between IOD/ENSO indices

2a. cmipEcIndeces
- plots of EcIndeces for each model to check the sign is correct and save the output

3. cmipEvents
- Calculate individal and compound events from the indeces

4. cmipCompounds
- Plot of compound event frequencies

5. cmipCompoundsImpact
- rainfall and temperature impacts from compound events

6. cmipImpact
- long term rainfall and temperautre trends, and impacts from individual events in different indeces
