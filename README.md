## Tree detection via LiDAR and RGB orthophoto data

This repository aims to work on the data proposed by the paper by Dubrovin, Fortin & Kedrov (2024).
The approach taken involves an algorithmic approach, similar to the one detailed on the paper, as well as a Machine Learning-centric approach for tree detection based on the datasets provided.

### Algorithmic approach
Using cdKtree, we use the UAV LiDAR data to check for local maxima of heights inside each plot via clustering and returning an average value for x, y and z for that specific cluster? this will be our tree top.

### Model approach
Use both UAV LiDAR data and RGB datasets to extract heights, intensity, r, g and b values to correlate to tree detections. We then use a Random Forest Classifier on these features to predict the probability of that specific combination of values being a tree top.