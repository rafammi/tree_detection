import pandas as pd 
import geopandas as gpd 
import matplotlib.pyplot as plt 
import seaborn as sns
import rasterio
import laspy
import numpy as np
from scipy.spatial import cKDTree

def detect(points,heights,plot_number):


    tree = cKDTree(points[:, :2])
    radius = 1.3 # test out different radius

    is_local_max = np.zeros(len(points), dtype=bool) # we declare a is_local_max with same length as the points
    for i, (x, y, z) in enumerate(points): #iterate over all points
        idx = tree.query_ball_point([x, y], radius) # we query to get idx
        if z >= np.max(heights[idx]): # if z is higher than the max height at that idx 
            is_local_max[i] = True # we set a local_max


    treetops = points[is_local_max] # filter out points that are local maxes - possible treetops
    print(f"Detected {len(treetops)} local maxima in plot {plot_number}")

    tree_tops = cKDTree(treetops[:, :2])
    _, nearest_top_idx = tree_tops.query(points[:, :2], k=1)

    cluster_labels = nearest_top_idx

    df = pd.DataFrame({
    "x": points[:, 0],
    "y": points[:, 1],
    "z": points[:, 2],
    "cluster": cluster_labels
    })

    fig, ax = plt.subplots(1,1)
    ax.scatter(df.x, df.y, c=df.cluster, s=1, cmap='tab20')
    ax.axis('equal')
    plt.savefig(f"images/{plot_number}/clusters.png")
    plt.close()

    treetops = (
    df.loc[df.groupby("cluster")["z"].idxmax(), ["cluster", "x", "y", "z"]]
    .reset_index(drop=True)
    )

    geometry = gpd.points_from_xy(treetops['x'], treetops['y'])
    tree_gdf = gpd.GeoDataFrame(treetops, geometry=geometry, crs="EPSG:32640")


    return treetops, tree_gdf
