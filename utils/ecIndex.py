import sys
sys.path.append('/../')

#import my functions
import helpers.fileHandler as fh
import utils.timePeriod as tp
import utils._modelDefinitions as _model
import utils._indexDefinitions as _index
import utils.sstIndex as sst



import xarray
import numpy
from eofs.xarray import Eof


def anoms(xr):
    '''Calculate an anomaly for the provided, using 1900 to 2000 climatology'''
    
    mean=xr.where((xr.time.dt.year>=1900) * (xr.time.dt.year<2000), 
                             drop=True).mean(dim='time')
    return xr-mean

def sstAnomsWang(tsXr):
    ''' This is how Wang/Cai calculate anomalies'''
    
    #Area of interest for ec Indeces
    tsXr=tsXr.where(
        (tsXr.lat>=-15) & (tsXr.lat<=15) &
        (tsXr.lon>=140) & (tsXr.lon<=280),
        drop=True
    )
    
    tsXr=tsXr.where(
        (tsXr.time.dt.year>=1900) & (tsXr.time.dt.year<2100), drop=True
    )

    
    #Rechunk so that time is all in one chunk. Not sure this is useful but it does seem to reduce memory needs
    tsXr=tsXr.chunk(-1, 'auto', 'auto')
    
    #Fit a quadratic and detrend using it
    trendXr = tsXr.polyfit('time', 2)
    trendXr = xarray.polyval(tsXr.time, trendXr.polyfit_coefficients, 'degree')
    detrendXr=tsXr-trendXr
    
    #calculate monthly anoms.
    sstAnomXr=detrendXr.groupby('time.month').apply(anoms)
    return sstAnomXr
    
def sstAnoms(tsXr, climatXr):
    ''' sst Anoms using two datasets provided'''
    
    #calculate average between -20 and 20 globall to detrend with
    trendXr=sst.calculateIndex(
                tsXr.to_dataset().assign_attrs({'project_id':'CMIP'}), 
                sst.calculateClimatology(climatXr.to_dataset().assign_attrs({'project_id':'CMIP'}))
                                ).backgroundSstNoDetrend.chunk('auto')
    
    #Area of interest for ec Indeces
    tsXr=tsXr.where(
        (tsXr.lat>=-15) & (tsXr.lat<=15) &
        (tsXr.lon>=140) & (tsXr.lon<=280),
        drop=True
    )
    
    climatXr=climatXr.where(
        (climatXr.lat>=-15) & (climatXr.lat<=15) &
        (climatXr.lon>=140) & (climatXr.lon<=280),
        drop=True
    )
    
    climatXr=climatXr.chunk([-1, 'auto', 'auto'])
    
    climatMeans=climatXr.groupby('time.month').mean(dim='time')
    
    #calculate monthly anoms.
    sstAnomXr=tsXr.groupby('time.month')-climatMeans
    
    #Rechunk so that time is all in one chunk. Not sure this is useful but it does seem to reduce memory needs
    sstAnomXr=sstAnomXr.chunk([-1, 'auto', 'auto'])
    
    #Fit a quadratic and detrend using it
    #trendXr = sstAnomXr.polyfit('time', 2)
    #trendXr = xarray.polyval(sstAnomXr.time, trendXr.polyfit_coefficients, 'degree')
    
    
    detrendXr=sstAnomXr-trendXr
    
    
    
    return detrendXr
    

def eofSolver(sstAnomXr): 
    
    sstAnomXr.load()
    
    #weights = numpy.cos(numpy.deg2rad(sstAnomXr.lat)
    #            ).values[..., numpy.newaxis]
    
    return Eof(sstAnomXr) #, weights=weights)


def ecIndex(sstAnomXr):
    import numpy.polynomial as poly
    
    
    solver=eofSolver(sstAnomXr)
    pcTimeXr=solver.pcs(npcs=2, pcscaling=1)
    
    djfAnomXr=tp.averageForTimePeriod(
            sstAnomXr.to_dataset(name='enso')).rename({'year':'time'}).enso.chunk('auto')

    solver=eofSolver(djfAnomXr)
    djfPcXr=solver.pcs(npcs=2, pcscaling=1)
    
    
    pc1 = pcTimeXr.sel(mode=0)
    pc2 = pcTimeXr.sel(mode=1)
    
    pFit = poly.Polynomial.fit(pc1, pc2, 2)
    alpha = pFit.convert().coef[2]
    
    eofsXr = solver.eofs(neofs=2) #eofscaling=1
    
    pFitDjf = poly.Polynomial.fit(djfPcXr.sel(mode=0), djfPcXr.sel(mode=1), 2)
    alphaDjf = pFitDjf.convert().coef[2]
    
    #cXr=(pcTimeXr.sel(mode=0)+pcTimeXr.sel(mode=1))/numpy.sqrt(2)
    #eXr=(pcTimeXr.sel(mode=0)-pcTimeXr.sel(mode=1))/numpy.sqrt(2)
        
    indeces = xarray.merge([pcTimeXr.sel(mode=0).drop('mode').rename('pc1'),
                            pcTimeXr.sel(mode=1).drop('mode').rename('pc2'), 
                            #eXr.rename('eIndex'),cXr.rename('cIndex')
                           ])
    indeces['alpha']=alpha
    indeces['alphaDjf']=alphaDjf
    
    return indeces, pFit, eofsXr





def ensoPlotter(da, ax):
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    import matplotlib.pyplot as plt 
    import numpy
    
    precContours=numpy.arange(-0.6,0.61,0.1)
    
    cs=plt.contourf(da.lon, da.lat, da.values, #precContours, 
                    transform=ccrs.PlateCarree(), cmap='coolwarm', #extend='both' ,
                   )

    gl=ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle=':')
    ax.coastlines(color='black')
    gl.top_labels=False
    #gl.left_labels=False

        #bottom legend
    cbar=plt.colorbar(orientation='horizontal', fraction=0.05, pad=0.05)

