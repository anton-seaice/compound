# compound

Developed using anaconda and python3

Incomplete list of dependencies

nc-time-axis (https://github.com/SciTools/nc-time-axis)
xarray
numpy
cartopy (https://scitools.org.uk/cartopy/docs/latest/)


To Run:

output from cesmIndeces is needed for everything else
output from cesmPrecTsMonthly is needed for cesmCompoundsImpact

Descriptions:

1. cesmIndeces
- Calculates monthly indeces (for indeces indluded in utils/_indexDefinitions.py)
- Calculates warm season averages (time periods defined in utils/_indexDefinitions.py)

2. cesmCompounds
- Plots of annual trends in enso, iod, sam
- Example of how events compound to be fire promoting or not-fire promoting
- Plots of 30 year trends in compounding events

3. cesmCompoundsType
- Plots of 30 years trends in compounding events, seperated by event type (i.e. on of the three pairs or all3)

4. cesmPrecTsMonthly
- Calculates warm season averages for prec and Ts

5. cesmCompoundImpacts
- Rainfall and Temp anomalies for each individial event type, and each compound event type


Useful git commands:

normal commit: git commit -m "message", git add
add changed files only: git add -u
tagging: git tag v1.0 ; git push --tags
