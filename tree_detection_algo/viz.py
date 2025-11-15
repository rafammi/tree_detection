
import geopandas as gpd 
import matplotlib.pyplot as plt 
import rasterio
from rasterio.io import DatasetReader
import rasterio.plot

def view_detections(plot_raster: DatasetReader, tree_gdf: gpd.GeoDataFrame, ground_truth: gpd.GeoDataFrame, plot_number: str) -> None:
    """ Visually compare detections vs gt

    Args:
        plot_raster: rgb ortho of specified plot number
        tree_gdf: gpdataframe containing detected grees
        ground_truth: filed survey for specified plot number
        plot_number: number of plot that is being evaluated to save image
    """


    fig, axes = plt.subplots(1, 2, figsize=(12,12))
    extent = [plot_raster.bounds[0], plot_raster.bounds[2], plot_raster.bounds[1], plot_raster.bounds[3]]
    ax = rasterio.plot.show(plot_raster, extent=extent, ax=axes[0])
    tree_gdf.plot(ax = axes[0])

    ax = rasterio.plot.show(plot_raster, extent=extent, ax=axes[1])
    ground_truth.plot(ax = axes[1])
    plt.savefig(f"images/{plot_number}/plot.png")
    plt.close()