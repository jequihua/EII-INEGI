# This is a sample Python script to write the EI index to a geotiff raster.
import gc
import misc_functions as mf
import numpy as np
import rasterio as rio
import pandas as pd
from pathlib import Path

def scale(m,minv,maxv,minlim,maxlim, decimals=2):
    scaled = ((m-minv)/(maxv-minv)*(maxlim-minlim))+minlim
    scaled = np.around(scaled, decimals=decimals)
    return scaled

PATHDVP = './IEE/1delt_vp.tif'
PATHEI = './IEexp/IE_expectedVal_INEGI_2023.csv'

if __name__ == '__main__':

    # Creat missing values mask.
    rast = rio.open(PATHDVP)
    vec = rast.read()[0,:,:]
    transform = rast.transform
    crs = rast.crs
    width = rast.width
    height = rast.height
    first_element = vec[0]
    mask = vec == first_element
    vec[mask]=np.nan

    # Load EI csv (expected value).
    ei_data = np.genfromtxt(PATHEI, delimiter=',', skip_header=1)
    ei_data = scale(ei_data,18,0,0,1)

    new_dataset = rio.open('./IEexp/IE_expectedVal_INEGI_2023.tif', 'w', driver='GTiff',
                                height=height, width=width,
                                count=1, dtype=str(vec.dtype),
                                crs=crs,
                                transform=transform)
    vec[~mask] = ei_data
    new_dataset.write(vec, 1)
    new_dataset.close()



