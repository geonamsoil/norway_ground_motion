Summary of the content of the jupyter notebooks:

* `plot_points.ipynb`

Script to load the ground motion data, select a point and plot it in a map. 

* `process_ground_motion.ipynb`

Analyse a test area of Norway from the Norwat InSAR ground motion data.
This will include timeseries for each of the points. Testing classification algorithms not very succesfully. 

* `sensitivity_regression_clustering_change_detection.ipynb`

Analyse a test area of Norway from the Norwat InSAR ground motion data.
Inclues regression, fourier series and change point detection. Main data analysis script. 

* `change_point_detection_frequency.ipynb`

Analyis of change point occurences. When do most happen? Can we see any patterns?

* `correlation_classification.ipynb`

Correlation between the different regression classes for ground motion. 

* `norway_1km_rainfall.ipynb`

Attempt to process the 1km Norway rainfall data. Dataset too big to process.

* `rainfall_timeseries_analysis.ipynb`

Main script to process the GPM rainfall data.

* `rainfall_widget_regression.ipynb`

Plot the GPM rainfall data on an interactive map.

* `all_data_widgets_insar_variables.ipynb`

Make interactive maps of the InSAR variables to check for any correlation with the ground motion time series data. 

* `data_IW1_IW2_regression_clustering.ipynb`

Combine the data `160-IW1-414-s1-asc1-v2020.csv` and `160-IW2-414-s1-asc1-v2020.csv`. Not sure what the differences are so having a look 