import pandas as pd 
import geopandas as gpd 
import matplotlib.pyplot as plt 
import seaborn as sns
import rasterio
import laspy
import numpy as np
from scipy.spatial import cKDTree

def detect(points: np.ndarray, heights: np.ndarray, plot_number: str) -> tuple[pd.DataFrame, gpd.GeoDataFrame]:
    """ Main algorithm for individual tree detection.

        Args:
            points: array of masked points from plot
            heights: array of masked heights used in processing

        Returns:
            treetops: a dataframe containing tree tops
            tree_gdf: a gdf containing tree tops as a single point
    """
    # Neighborhood structure in k-tree to look for neighbors


    adaptive_radii = {
    "01": 1.421053,
    "02": 1.368421,
    "03": 1.526316,
    "04": 1.736842,
    "05": 1.842105,
    "06": 1.789474,
    "07": 1.421053,
    "08": 1.421053,
    "09": 1.052632,
    "10": 1.157895
    }
    radius = adaptive_radii[plot_number]
    tree = cKDTree(points[:, :2])

    is_local_max = np.zeros(len(points), dtype=bool) # we declare a is_local_max with same length as the points
    seen_mask = np.zeros(len(points), dtype=bool)
    for i, (x, y, z) in enumerate(points): #iterate over all points

        # for the current point, return all indices within the euclidean distance defined by radius
        idx = tree.query_ball_point([x, y], radius)
        highest_neighbor = idx[np.argmax(heights[idx])]
        # if index j is higher, set as local maximum
        seen_mask[idx] = True
        seen_mask[highest_neighbor] = False 
        if i == highest_neighbor:
            is_local_max[i] = True

    # we get the points considered local maximum
    treetops = points[is_local_max] # filter out points that are local maxes - possible treetops
    print(f"Detected {len(treetops)} local maxima in plot {plot_number}")

    # on top of thiese max points we get another k-tree
    tree_tops = cKDTree(treetops[:, :2]) # query for points that were classfied as potential tree tops
    _, nearest_top_idx = tree_tops.query(points[:, :2], k=1) # get index of nearest tree top

    # we define cluster as points that belong to that nearest possible treetop
    cluster_labels = nearest_top_idx

    # create dataframe
    df = pd.DataFrame({
    "x": points[:, 0],
    "y": points[:, 1],
    "z": points[:, 2],
    "cluster": cluster_labels
    })

    # we plot how the clustering looks, this will eventually become one single point
    fig, ax = plt.subplots(1,1)
    ax.scatter(df.x, df.y, c=df.cluster, s=1, cmap='tab20')
    ax.axis('equal')
    plt.savefig(f"images/{plot_number}/clusters.png")
    plt.close()

    # this might not be the best way to cluster these points together but we get
    # the maximum value of z and assume that it is most likely
    # the tree top around that cluster
    # we then take the value of x, y and z make a df containing that info
    treetops = (df.loc[df.groupby("cluster")["z"].idxmax(),
        ["cluster", "x", "y", "z"]].reset_index(drop=True))

    # normal geopandas stuff to create a gdf
    geometry = gpd.points_from_xy(treetops['x'], treetops['y'])
    tree_gdf = gpd.GeoDataFrame(treetops, geometry=geometry, crs="EPSG:32640")


    return treetops, tree_gdf
