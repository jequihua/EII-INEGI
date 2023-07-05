"""
    This is a sample Python script to load all rasters into a table
    for the calculation of the EI index.
"""
import gc
import misc_functions as mf
import numpy as np
import rasterio as rio
from pathlib import Path

PATHDVP = '../RASTER/raster_entrega/1delt_vp.tif'
PATHR = '../RASTER/raster_entrega/'

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
        vec[np.isnan(vec)] = -999.0
        vec = vec.astype(str)
        vec[vec=="-999.0"] = "*"
        out_numpy[:,file_idx] = vec

    del mask
    del vec
    gc.collect()

    # Netica necesita nombres ASCII y los nodos no pueden empezar con número
    raster_names_list = [n.replace("1delt", "delt").replace("ñ", "n") for n in raster_names_list]

    names = np.array(raster_names_list, dtype='str')
    out_numpy = np.vstack((names, out_numpy))

    """
        Datos faltantes?
        ntervalo -3.4028234663852886e+38
        MDE2 -32768
        AgrPC_Final 255
        ArbHa_Final2 255
        ArbM_Final2 255
        Asentam_human_fixed -3.3999999521443642e+38
        BMM_Final 255
        Cobert_bosque 127
        Cobert_matorr 127
        Cobert_selva 127
        DañIns_Final2 255
        DesvAFL_Final2 255
        DesvAT_Final2 255
        DesvDAP_Final2 255
        DesvDiamC_Final2 255
        PromAFL_Final2 255
        PromAT_Final2 255
        PromDAP_Final2 255
        PromDC_Final2 255
        SinVeg_Final1 255
        Zonas_vida1 -128
    """

    np.savetxt("ei_inegi_traintable_2.csv", out_numpy, fmt='%s', delimiter=',')



