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


    gt_coords = [[geom.x, geom.y] for geom in ground_truth.geometry]
    gt = np.array(gt_coords)

    detected_coords = [[geom.x, geom.y] for geom in tree_gdf.geometry]
    detected = np.array(detected_coords)

    if len(detected) == 0 or len(gt) == 0:
        return 0, 0, 0
        
    tree_gt = cKDTree(gt[:, :2])
    matches = 0
        
    for det_tree in detected:
        dist, _ = tree_gt.query(det_tree[:2])
        if dist <= max_dist:
            matches += 1
        
    recall = matches / len(gt)
    precision = matches / len(detected)
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
    gt_num = len(gt)
    detected_num = len(detected)
    return recall, precision, f1, gt_num, detected_num