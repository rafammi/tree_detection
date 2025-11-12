import numpy as np 
import scipy


def normalize_cloud_height(las):
    LAS_GROUND_CLASS = 2
    out = las.xyz.copy()
    assert np.any(las.classification == LAS_GROUND_CLASS)
    ground_level = scipy.interpolate.griddata(
        points=las.xyz[las.classification == LAS_GROUND_CLASS, :2],
        values=las.xyz[las.classification == LAS_GROUND_CLASS, 2],
        xi=las.xyz[:, :2],
        method="nearest",
    )
    out[:, 2] -= ground_level
    return out