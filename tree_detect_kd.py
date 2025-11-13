from pathlib import Path
import geopandas as gpd
import csv
import numpy as np
import pandas as pd
import scipy 

from tree_detection_algo.detect import detect
from tree_detection_algo.filter import filter_ground
from tree_detection_algo.load import load
from tree_detection_algo.viz import view_detections
from tree_detection_algo.evaluate import calculate_metrics
from tree_detection_algo.normalize import normalize_cloud_height
from tree_detection_algo.match import match_candidates

def crop_by_other(points: np.ndarray, other: np.ndarray) -> np.ndarray:
    """Crop points by the extent of other."""
    hull = scipy.spatial.ConvexHull(other[:, :2])
    vertex_points = hull.points[hull.vertices]
    delaunay = scipy.spatial.Delaunay(vertex_points)
    within_hull = delaunay.find_simplex(points[:, :2]) >= 0
    return points[within_hull]

def process_plot(plot_number: str):
    """ Main function to put everything together

        Args:
            plot_number: plot to be processed

        Returns:
            recall: recall score for plot
            precision: precision score for plot
            f1: harmonic mean of recall and precision for plot
            gt_num: count of ground truth trees
            detected_num: treetops detected
    """

    print(f"Processing plot {plot_number}...")
    plot_las, plot_raster, field_survey, ground_truth = load(plot_number)

    plot_las = normalize_cloud_height(plot_las)

    points, heights = filter_ground(plot_las, 2)

    treetops, tree_gdf = detect(points,heights,plot_number)


    gt = np.column_stack((ground_truth.geometry.x, ground_truth.geometry.y, ground_truth["height"]))
    candidates = treetops[["x", "y", "z"]].to_numpy()

    candidates = crop_by_other(candidates, gt)

    out = match_candidates(gt, candidates, max_distance = 5, max_height_difference=3)
    out_df = pd.DataFrame(out)

    metrics = pd.DataFrame(calculate_metrics(out_df))

    view_detections(plot_raster, tree_gdf, ground_truth, plot_number)

    return metrics

def main():
    plot_ids = [f"{i:02d}" for i in range(1, 11)]

    results = []

    for pid in plot_ids:
        try: 
            metrics = process_plot(pid)
            metrics["pid"] = pid
            results.append(metrics)
        except Exception as e:
            print(f"Error in {pid} - {e}")
    
    if results:
        final_report = pd.concat(results, ignore_index=False)
        final_report.to_csv("output_adaptive.csv")
    else:
        print("Error in report generation")

if __name__ == "__main__":
    main()