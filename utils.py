import sys
sys.path.append('/home/b/b381815/python_functions/')

import os
import xarray as xr
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from healpix_functions import aggregate_grid_xarray, sub_grid_anomaly_xarray, evaluate_against_coarse_xarray, _guess_gridn
from etccdi_dict import etccdi_indices


dpi = 2000
mpl.rc('font', **{'size': 6})
proj = ccrs.Mollweide()
proj._threshold /= 10000.
cm = 1/2.54  # centimeters in inches

path = '/work/uc1275/LukasBrunner/data/SubGridVariability/4wdc'
figpath = '../figures_all'


def get_ax():
    fig, ax = plt.subplots(figsize=(8*cm, 4*cm), dpi=dpi, subplot_kw={'projection': proj})
    fig.subplots_adjust(left=.01, bottom=.01)
    ax.set_global()
    return fig, ax


def calc_cases(icon_z9, icon_z6, ifs_z9, ifs_z6):
    cases = {
        'icon': {
            'z9': icon_z9.mean('time'),
            'z6': icon_z6.mean('time'),
            # 'z9_mean_z6': aggregate_grid_xarray(icon_z9, z_out=6, method='mean').mean('time'),
            # sub-grid cases: index calculation first
            'z9_std_z6': aggregate_grid_xarray(icon_z9, z_out=6, method='std').mean('time'),
            'z9_cv_z6': aggregate_grid_xarray(icon_z9, z_out=6, method='cv').mean('time'),
            'z9_anom_z9': sub_grid_anomaly_xarray(icon_z9, z_coarse=6).mean('time'),   
            # sub-grid cases: regridding first
            'z9-z6_anom_z9': evaluate_against_coarse_xarray(icon_z9, icon_z6).mean('time'),
        },
        'ifs': {
            'z9': ifs_z9.mean('time'),
            'z6': ifs_z6.mean('time'),
            # 'z9_mean_z6': aggregate_grid_xarray(ifs_z9, z_out=6, method='mean').mean('time'),
            # sub-grid cases: index calculation first
            'z9_std_z6': aggregate_grid_xarray(ifs_z9, z_out=6, method='std').mean('time'),
            'z9_cv_z6': aggregate_grid_xarray(ifs_z9, z_out=6, method='cv').mean('time'),
            'z9_anom_z9': sub_grid_anomaly_xarray(ifs_z9, z_coarse=6).mean('time'),   
            # sub-grid cases: regridding first
            'z9-z6_anom_z9': evaluate_against_coarse_xarray(ifs_z9, ifs_z6).mean('time'),
        },
    }

    return cases


def get_cases(index):
    fn_icon_z9 = os.path.join(path, 'ICON-ngc4008', 'z9', f'{index}_ann_ICON-ngc4008_ssp370_zoom9.nc')
    fn_icon_z6 = os.path.join(path, 'ICON-ngc4008', 'z6', f'{index}_ann_ICON-ngc4008_ssp370_zoom6.nc')
    fn_ifs_z9 = os.path.join(path, 'IFS-9-FESOM-5-production', 'z9', f'{index}_ann_IFS-9-FESOM-5-production_ssp370_zoom9.nc')
    fn_ifs_z6 = os.path.join(path, 'IFS-9-FESOM-5-production', 'z6', f'{index}_ann_IFS-9-FESOM-5-production_ssp370_zoom6.nc')

    icon_z9 = xr.open_dataset(fn_icon_z9, decode_timedelta=False)[index].load()
    icon_z6 = xr.open_dataset(fn_icon_z6, decode_timedelta=False)[index].load()
    if index in ['tasmin', 'tasmax', 'pr']:  # base variables are daily
        icon_z9 = icon_z9.resample(time='1Y').mean()
        icon_z6 = icon_z6.resample(time='1Y').mean()
    
    ifs_z9 = xr.open_dataset(fn_ifs_z9, decode_timedelta=False)[index].load()
    ifs_z6 = xr.open_dataset(fn_ifs_z6, decode_timedelta=False)[index].load()
    if index in ['tasmin', 'tasmax', 'pr']:
        ifs_z9 = ifs_z9.resample(time='1Y').mean()
        ifs_z6 = ifs_z6.resample(time='1Y').mean()

    # keeping these breaks xarrays apply_ufunc
    icon_z9 = icon_z9.drop(['lon', 'lat', 'crs'])
    icon_z6 = icon_z6.drop(['lon', 'lat', 'crs'])
    ifs_z9 = ifs_z9.drop(['lon', 'lat', 'crs'])
    ifs_z6 = ifs_z6.drop(['lon', 'lat', 'crs'])

    return calc_cases(icon_z9, icon_z6, ifs_z9, ifs_z6)