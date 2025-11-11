
import numpy as np 

def filter_ground(plot_las, percentile):
    """ Function that filters ground points from .las file
    
    Args:
        plot: object derived from loading of .las file
        percentile: used to define percentile of ground points

    Returns:
        points: masked points from plot
        heigjts: masked heights used in processing
    """

    points = np.vstack((plot_las.x, plot_las.y, plot_las.z)).T
    heights = points[:, 2]
    min_z = np.percentile(heights, percentile) #filter ground points - test different percentiles
    mask = heights > min_z
    points = points[mask]
    heights = heights[mask]

    return points, heights