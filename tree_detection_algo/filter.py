
import numpy as np 
from laspy import LasData

def filter_ground(plot_las: LasData, percentile: int) -> tuple[np.ndarray, np.ndarray]:
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
    min_z = np.percentile(heights, percentile) # filter ground points - test different percentiles
    mask = heights > min_z # I didn't normalize
    # I do understand that is common practice, but no matter how much I tweaked different parameters for detection
    # normalization shot the number of possible tree tops way too high
    points = points[mask]
    heights = heights[mask]

    return points, heights