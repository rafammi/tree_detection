
import collections
import pandas as pd 

def calculate_metrics(group):
    """Function to evaluate metrics of detected vs ground_truth

    This was pulled directly from the 2024 paper as to have a fair comparison
    between algorithms. All credits are to the original authors
    
    Args:
        group: a dataframe structure containing the class of detection
        TP, FP, TN, FN
    Returns: 
        a pd.series with the aggregated metrics: F1, recall, precision and avg_distance between points

    """
    classes = collections.Counter(group["class"])
    metrics = {
        "recall": classes["TP"] / (classes["TP"] + classes["FN"]),
        "precision": classes["TP"] / (classes["TP"] + classes["FP"]),
    }
    if metrics["recall"] + metrics["precision"] > 0:
        metrics["f1"] = 2 * metrics["recall"] * metrics["precision"]
        metrics["f1"] = metrics["f1"] / (metrics["recall"] + metrics["precision"])
    else:
        metrics["f1"] = 0
    metrics["avg_dist"] = group["distance"].mean()
    return round(pd.Series(metrics), 2)