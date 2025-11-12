from scipy.spatial import cKDTree
import numpy as np
import geopandas as gpd 
import collections
import pandas as pd 

def calculate_metrics(group):
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