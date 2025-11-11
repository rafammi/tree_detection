from pathlib import Path
import geopandas as gpd
import csv


from tree_detection_algo.detect import detect
from tree_detection_algo.filter import filter_ground
from tree_detection_algo.load import load
from tree_detection_algo.viz import view_detections
from tree_detection_algo.evaluate import evaluate


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
    plot_las, plot_raster, gt, ground_truth = load(plot_number)

    points, heights = filter_ground(plot_las, 5)

    treetops, tree_gdf = detect(points,heights,plot_number)

    recall, precision, f1, gt_num, detected_num = evaluate(tree_gdf, ground_truth, max_dist = 5.0)

    view_detections(plot_raster, tree_gdf, ground_truth, plot_number)

    return recall, precision, f1, gt_num, detected_num

def main():
    plot_ids = [f"{i:02d}" for i in range(1, 11)]

    results = []

    for pid in plot_ids:
        try: 
            recall, precision, f1, gt_num, detected_num = process_plot(pid)
            results.append({
                "plot_id": pid,
                "recall": recall,
                "precision": precision,
                "f1": f1,
                "gt_num": gt_num,
                "detected_num": detected_num,
            })
        except Exception as e:
            print(f"Error in {pid} - {e}")
    
    output = "results.csv"

    with open(output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["plot_id", "recall", "precision", "f1",
                                                "gt_num", "detected_num"])
        writer.writeheader()
        writer.writerows(results)

    print(f"Metrics exported to {output}")

if __name__ == "__main__":
    main()