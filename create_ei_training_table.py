# This is a sample Python script to load all rasters into a table for the calculation of the EI index.
import gc
import misc_functions as mf
import numpy as np
import rasterio as rio
import pandas as pd
from pathlib import Path

PATHDVP = './IEE/1delt_vp.tif'
PATHR = './IEE/'

if __name__ == '__main__':

    files = mf.multiple_file_types(PATHR, ["*.tif"], recursive=True)
    files_ = list(files)

    raster_list = []
    raster_names_list = []

    # Creat missing values mask, the raster 1delt_vp.tif will be the reference.
    vec = rio.open(PATHDVP).read().flatten()
    
    first_element = vec[0]
    mask = vec == first_element

    out_numpy = np.empty((np.sum(~mask),len(files_)), dtype="<U10")

    for file_idx, file_path in enumerate(files_):
        print(file_path)
        raster_names_list.append(Path(file_path).stem)
        vec = rio.open(file_path).read().flatten().astype(np.float64)
        first_element = np.around(vec[0], decimals=2)
        vec = np.around(vec[~mask], decimals=2)
        vec[vec==first_element] = -999.0
        vec = vec.astype(str)
        vec[vec=="-999.0"] = "*"
        out_numpy[:,file_idx] = vec

    del mask
    del vec
    gc.collect()

    names = np.array(raster_names_list, dtype='str')
    out_numpy = np.vstack((names, out_numpy))

    np.savetxt("ei_inegi_traintable.csv", out_numpy, fmt='%s', delimiter=',')



