import numpy as np
import xarray as xr
import healpy as hp


def aggregate_grid(arr: np.ndarray, z_out: int, method: str='mean') -> np.ndarray:
    """Spatially aggregate to a coarser grid.

    Parameters
    ----------
    arr : np.ndarray, shape (M,)
        The length of the array M has to be M = 12 * (2**zoom)**2
    z_out : int
        Healpix zoom level of the output grid. Needs to be smaller than the input zoom level.
    method : str, optional by default 'mean'
        Spatial aggregation method. 
        - 'mean': Mean of sub-grid cells -> conservative regridding
                  This is equivalent to `healpy.ud_grade`
        - 'std': Standard deviation of sub-grid cells
        - 'min': Minimum of sub-grid cells
        - 'max': Maximum of sub-grid cells

    Returns
    -------
    np.ndarray, shape (N < M,)

    Info
    ----
    Zoom levels in healpix (Hierarchical Equal Area isoLatitude Pixelization of a sphere)
    https://healpy.readthedocs.io/en/latest/index.html
    https://healpix.jpl.nasa.gov/index.shtml

    Zoom level 0 divides the globe into 12 grid cells, each zoom level
    increase increases the number of cells by 4 and half the resolution
    in kilometer

    nside = 2**zoom
    nr. cells = 12 * nside**2

    | zoom | nside | res. (km) | nr. cells  |
    | ---- | ----- | --------- | ---------- |
         0 |     1 |    6519.6 | 12
         1 |     2 |    3259.8 | 48
         2 |     4 |    1629.9 | 192
         3 |     8 |     815.0 | 768
         4 |    16 |     407.5 | 3,072
         5 |    32 |     203.7 | 12,288
         6 |    64 |     101.9 | 49,152
         7 |   128 |      50.9 | 196,608
         8 |   256 |      25.5 | 786,432
         9 |   512 |      12.7 | 3,145,728
        10 |  1024 |       6.4 | 12,582,912
        11 |  2048 |       3.2 | 50,331,648
        12 |  4096 |       1.6 | 201,326,592
    """
    npix_in = arr.size
    npix_out = hp.nside2npix(2**z_out)
    
    if npix_out >= npix_in:
        raise ValueError('Outuput zoom level needs to be smaller than input zoom level')

    ratio = npix_in / npix_out
    if not ratio.is_integer():  # this should never happen
        raise ValueError(f'{ratio=}')
    else:
        ratio = int(ratio)
    
    if method == 'mean':
        return arr.reshape(npix_out, ratio).mean(axis=-1)
    if method == 'std':
        return arr.reshape(npix_out, ratio).std(axis=-1)
    if method == 'min':
        return arr.reshape(npix_out, ratio).min(axis=-1)
    if method == 'max':
        return arr.reshape(npix_out, ratio).max(axis=-1)
    if method == 'cv':
        return arr.reshape(npix_out, ratio).std(axis=-1) / arr.reshape(npix_out, ratio).mean(axis=-1)
        
    raise ValueError(f'{method=}')


def _guess_gridn(da):
    """Try to gess the name of the spatial coordinate name from a list of frequent options."""
    dims = list(da.dims)
    gridn = []
    if 'values' in dims:
        gridn.append('values')
    if 'value' in dims:
        gridn.append('value')
    if 'cell' in dims:
        gridn.append('cell')
    if 'x' in dims:
        gridn.append('x')
    if len(gridn) == 1:
        return gridn[0]

    raise ValueError('gridn needs to be set manually to one of: {}'.format(', '.join(dims)))


def aggregate_grid_xarray(da: xr.DataArray, z_out: int, method: str='mean', gridn=None) -> xr.DataArray:
    """Thin xarray wrapper for `aggregate_grid'."""
    
    if gridn is None:  # try to guess grid name from frequent options
        gridn = _guess_gridn(da)
            
    return xr.apply_ufunc(
        aggregate_grid,
        da, z_out,
        input_core_dims=[[gridn], []],
        output_core_dims=[['tmp']],
        vectorize=True,
        kwargs={'method': method},
    ).rename({'tmp': gridn})


def evaluate_against_coarse(fine: np.ndarray, coarse: np.ndarray) -> np.ndarray:
    """Evaluate the fine grid against a coarser grid. Output on the fine grid.

    Parameters
    ----------
    fine : np.ndarray, shape (M,)
    coarse : np.ndarray, shape (N<M,)

    Returns
    -------
    np.ndarray, shape (M,)
    """
    npix_fine = fine.size
    npix_coarse = coarse.size

    if npix_coarse > npix_fine:
        raise ValueError('`fine` needs to have a higher zoom level than `coarse`')

    ratio = npix_fine / npix_coarse 
    if not ratio.is_integer():
        raise ValueError(f'{ratio=}')

    return (fine.reshape(npix_coarse, int(ratio)) - coarse.reshape(npix_coarse, 1)).ravel()


def evaluate_against_coarse_xarray(da_fine, da_coarse, gridn=None):
    """Thin xarray wrapper for `evaluate_against_coarse`."""
    if gridn is None:  # try to guess grid name from frequent options
        gridn_fine = _guess_gridn(da_fine)
        gridn_coarse = _guess_gridn(da_coarse)

    return xr.apply_ufunc(
        evaluate_against_coarse,
        da_fine, da_coarse.rename({gridn_coarse: 'tmp'}),
        input_core_dims=[[gridn_fine], ['tmp']],
        output_core_dims=[[gridn_fine]],
        vectorize=True,
    )


def sub_grid_anomaly(arr: np.ndarray, z_coarse: int) -> np.ndarray:
    """

    Parameters
    ----------
    arr : np.ndarray, shape (M,)
    z_coarse : int
        Healpix zoom level of the coarser grid. Needs to be smaller than the input zoom level.


    Returns
    -------
    np.ndarray, shape (N < M,)
    """
    arr_coarse = aggregate_grid(arr, z_coarse, 'mean')
    return evaluate_against_coarse(arr, arr_coarse)


def sub_grid_anomaly_xarray(da: xr.DataArray, z_coarse, gridn=None, **kwargs: dict) -> xr.DataArray:
    """xarray wrapper for `sub_grid_anomaly'."""
    if gridn is None:  # try to guess grid name from frequent options
        gridn = _guess_gridn(da)
                
    return xr.apply_ufunc(
        sub_grid_anomaly,
        da, z_coarse,
        input_core_dims=[[gridn], []],
        output_core_dims=[[gridn]],
        vectorize=True,
        kwargs=kwargs,
    )


def attach_grid_info(da: xr.DataArray, gridn=None, return_latlon=False) -> xr.Dataset:
    """Attach to longitude and latitude values of each grid cell to the Dataset.

    Parameters
    ----------
    da : xr.DataArray
    gridn : string, optional, by default None
        String specifying the name of the grid variable. If None, try to guess it from frequent options
    return_latlon: bool, optional, by default False
        If True, return the grid values as xr.DataArrays instead of creating a xr.Dataset and attaching them.

    Returns
    -------
    xr.Dataset
        Dataset with the grid information attached as two new variables.
    """
    if gridn is None:  # try to guess grid name from frequent options
        gridn = _guess_gridn(da)
        
    lon, lat = hp.pix2ang(hp.npix2nside(da[gridn].size), da[gridn].values, nest=True, lonlat=True) 
    lon = xr.DataArray(
        lon, 
        coords={gridn: da[gridn].values},
        attrs={'units': 'degree_east', 'long_name': 'longitude', 'standard_name': 'longitude'},
    )

    lat = xr.DataArray(
        lat, 
        coords={gridn: da[gridn].values},
        attrs={'units': 'degree_north', 'long_name': 'latitude', 'standard_name': 'latitude'},
    )

    if return_latlon:
        return lat, lon

    da.attrs.update({
        'coordinates': 'lat lon',
        'gridType': 'healpix',
    })
    ds = da.to_dataset()
    ds['lon'] = lon
    ds['lat'] = lat
    return ds


def get_indices_in_rectangle(da, corners, inclusive=True):
    """
    Get indices for grid cells within a defined rectangle.
    
    Parameters
    ----------
    da : xr.DataArray
    corners : list of tuple (lon, lat)

    Returns
    -------
    idx : np.ndarray
    """    
    if len(corners) != 4:
        raise NotImplementError('Polygon has to be a rectangle')
    lon1, lat1 = corners.min(axis=0)
    lon2, lat2 = corners.max(axis=0)
    if inclusive:
        return np.where(
            ((da['lon'] >= lon1) & (da['lon'] <= lon2) &
             (da['lat'] >= lat1) & (da['lat'] <= lat2)), 
        )[0]
    return np.where(
        ((da['lon'] > lon1) & (da['lon'] < lon2) &
         (da['lat'] > lat1) & (da['lat'] < lat2)), 
    )[0]


def select_rectangle(da, corners, drop=False):
    """
    Mask or drop grid cells outside a defined rectangle.
    
    Parameters
    ----------
    da : xr.DataArray
    corners : list of tuple (lon, lat)
    drop : bool, optional, by default False
        Setting this to True will drop values outside the rectangle
        NOTE: this is often not what we want as it will no longer be
        possible to plot.

    Returns
    -------
    same as input
    """
    idx = get_indices_in_rectangle(da, corners)
    return da.where(da['values'].isin(idx), drop=drop)
