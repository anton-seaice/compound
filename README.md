# compound

This is a collection of scripts to examine changing frequenices of compounding impacts from multiple climate drivers upon mainland South East Australia.

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


To Run:

output from cesmIndeces is needed for everything else
output from cesmPrecTsMonthly is needed for cesmCompoundsImpact

Descriptions:

1. cesmIndeces
- Calculates monthly indeces (for indeces included in utils/_indexDefinitions.py)
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
