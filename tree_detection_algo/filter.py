
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

    heights = plot_las[:, 2]
    min_z = 3
    mask = heights > min_z
    points = plot_las[mask]
    heights = heights[mask]

    return points, heights