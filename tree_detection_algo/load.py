import laspy 
import rasterio
import pandas as pd
import geopandas as gpd
import rasterio

def load(plot_number):
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
    gt = gpd.read_file("/home/rafael/Projetos/tree_detection/data/field_survey.geojson")
    ground_truth = gt.query(f"plot=={int(plot_number.lstrip("0") or "0")}")

    return plot_las, plot_raster, gt, ground_truth