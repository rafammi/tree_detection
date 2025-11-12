import laspy 
from laspy import LasData
import rasterio
from rasterio.io import DatasetReader
import pandas as pd
import geopandas as gpd
import rasterio

def load(plot_number: str) -> tuple[LasData, DatasetReader, gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """ Loads data from specified plot number

    Args:
        plot_number: string for plot number to be loaded
        should follow structured of data: 01, 02, etc
    
    Returns:
        plot_las: las file for specified plot number
        plot_raster: rgb ortho of specified plot number
        ground_truth: filed survey for specified plot number
    """

    plot_las = laspy.read(f"/home/rafael/Projetos/tree_detection/data/als/plot_{plot_number}.las")
    plot_raster = rasterio.open(f"/home/rafael/Projetos/tree_detection/data/ortho/plot_{plot_number}.tif")
    field_survey = gpd.read_file("/home/rafael/Projetos/tree_detection/data/field_survey.geojson")
    ground_truth = field_survey.query(f"plot=={int(plot_number.lstrip("0") or "0")}")

    return plot_las, plot_raster, field_survey, ground_truth