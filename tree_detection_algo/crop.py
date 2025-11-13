import numpy as np
import scipy


def crop_by_other(points: np.ndarray, other: np.ndarray) -> np.ndarray:
    """Crop points by the extent of other.
    
    This is pulled directly from the 2024 paper. All credit to authors

    Args:
        points: a 3d array of points (x,y,z)
        other: a 3d array of points (x,y,z)
    Returns:
        points: points that are within the hull created by other    
    
    """
    # Define a hull by the second array of points
    hull = scipy.spatial.ConvexHull(other[:, :2])

    # Basically getting a bounding box
    vertex_points = hull.points[hull.vertices]

    # Delaunay triangulation
    delaunay = scipy.spatial.Delaunay(vertex_points)

    # Find which detected piints are inside the delaunay triangulation with (x, y)
    within_hull = delaunay.find_simplex(points[:, :2]) >= 0
    return points[within_hull]
