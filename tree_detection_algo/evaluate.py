from scipy.spatial import cKDTree
import numpy as np

def evaluate(tree_gdf, ground_truth, max_dist=5.0):
    """ Function that evaluates detections.

    This taken directly off of one kaggle contribution by HEDI FEKI
    (https://www.kaggle.com/code/hedifeki/tree-detection).
    All credits belong to original author 

    Args:
        detected: trees detected by algorithm
        ground_truth: coordinates of trees from field_survey for that plot
        max_dist = distance to consider for counting of trees (match or no match)

    Returns:
        recall: recall score of detected trees
        f1: f1 score of detected trees
        precision: precision score of detected trees

    """


    gt_coords = np.array([[geom.x, geom.y] for geom in ground_truth.geometry])
    det_coords = np.array([[geom.x, geom.y] for geom in tree_gdf.geometry])
    
    if len(det_coords) == 0 or len(gt_coords) == 0:
        return 0, 0, 0, len(gt_coords), len(det_coords)
    
    tree_gt = cKDTree(gt_coords)
    matched_gt = set()
    matches = 0
    
    for det in det_coords:
        dist, idx = tree_gt.query(det, distance_upper_bound=max_dist)
        # Check if valid match was done as this was inflating the metrics
        if dist <= max_dist and idx not in matched_gt:
            matches += 1
            matched_gt.add(idx)
    
    recall = matches / len(gt_coords)
    precision = matches / len(det_coords)
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return recall, precision, f1, len(gt_coords), len(det_coords)