import pandas as pd 
import geopandas as gpd 
import matplotlib.pyplot as plt 
import numpy as np
from scipy.spatial import cKDTree

def detect(points: np.ndarray, heights: np.ndarray, plot_number: str) -> tuple[pd.DataFrame, gpd.GeoDataFrame]:
    """ Main algorithm for individual tree detection.

        This uses the cKDtree neighborhood structure to query
        for potential treetops and cluster points together 
        based on local maxima

        Args:
            points: array of masked points from plot
            heights: array of masked heights used in processing

        Returns:
            treetops: a dataframe containing tree tops
            tree_gdf: a gdf containing tree tops as a single point
    """

    # These radius were defined empirically as to
    # maximize the f1 for each plot
    # some plots have denser point clouds while others
    # have sparser points
    adaptive_radii = {
     "01": 1.421053,
     "02": 1.368421,
     "03": 1.526316,
     "04": 1.736842,
     "05": 1.33,
     "06": 1.22,
     "07": 1.11,
     "08": 1.11,
     "09": 1.11,
     "10": 1.00
     }
    radius = adaptive_radii[plot_number]

    tree = cKDTree(points[:, :2])
    sorted_indices = np.argsort(heights)[::-1]
    is_local_max = np.zeros(len(points), dtype=bool) # we declare a is_local_max with same length as the points
    for idx in sorted_indices:
        if is_local_max[idx]:  # Skip if already processed as part of another tree
            continue
        x, y, z = points[idx, 0], points[idx, 1], points[idx, 2]
        neighbors = tree.query_ball_point([x, y], radius)
        if idx == neighbors[np.argmax(heights[neighbors])]: # if we're at the maximum index
            is_local_max[idx] = True
            is_local_max[neighbors] = False
            is_local_max[idx] = True # that means the neighbor is not the max

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

    # filter ou weak clusters. Not sure on the point quantity
    cluster_counts = df.groupby('cluster').size()
    valid_clusters = cluster_counts[cluster_counts >= 20].index
    df = df[df.cluster.isin(valid_clusters)].copy()

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
    treetops = df.groupby("cluster").apply(
        lambda g: pd.Series({
            'cluster': g.name,
            'x': g.loc[g['z'].idxmax(), 'x'],  # x,y from highest point
            'y': g.loc[g['z'].idxmax(), 'y'],
            'z': g['z'].quantile(0.98)  # using the 98th percentile as it felt possible that I
            # was missing matches due to height differences, but not sure.
        })
    ).reset_index(drop=True)

    # normal geopandas stuff to create a gdf
    geometry = gpd.points_from_xy(treetops['x'], treetops['y'])
    tree_gdf = gpd.GeoDataFrame(treetops, geometry=geometry, crs="EPSG:32640")


    return treetops, tree_gdf
