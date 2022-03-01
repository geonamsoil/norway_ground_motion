# Extra scope for Norway ground motion data

Here are a few points that would be worth expanding on:

* Download a larger region of Norway and apply the analysis to more data points.

* Add GPM rainfall information for a larger region. Currently the test region is too small given the resolution of the rainfall data. A larger area of Norway is needed to explore any correlation between the timeseries of precipitation and ground motion.

* Explore how the NASA GPM data compares to the 1km resolution Norway rainfall data from seNorge_2018. What is the optimal resolution of the data? For the European Ground motion service we will only have the NASA GPM data, how will the results compare to having 1km ainfall data, like they do in Norway? 

* Perform further analysis on finding seasonality and trends in the ground motion time series data. The current Fourier analysis is extremely limited and not reliable. Need to explore how to decouple the trends for irregularly spaced data.

* Study the behaviour of clusters of points. Do we find mostly that all points in a region behave similarly or is the point behaviour more independent?

* How far in advance do we need data to study the future behaviour of a point?

* Is the data biased because of the acquisition parameters of the satellite?

* Further analysis of Change Points. The python package `ruptures` has a few algorithms for this. It would be good to test each of them and see which ones work best and with what parameters.

* Incorporation of more datasets in the analysis such as geology layers, the road network or the slope of the terrain. Study the correlation of these parameters with the ground motion.

* Sensitivity analysis of the regression for ground motion data. The threshold parameters that I have chosen to discriminate between the 4 regression types are quite arbitrary. A more formal analysis of the optimal threshold would make the classification more reliable.

* Increase he complexity of the classification. If we incorporate new parameters such as geology or distance to roads, should we have a more complex classification model? How would this be implemented?

* Investigate the spread in the ground motion measurements. There are very large fluctuations in the measurements of the data. Where do they come from? How much do we need to account for in the classification?


* There is extra data on Landslide susceptibility for the whole of Norway available from the website [geonorge.no](https://www.geonorge.no/en). It would be interesting to look at this data and see how the precipitation patterns or geology match in with areas of high or low susceptibility.

* The website [geonorge.no](https://www.geonorge.no/en) has lots of data available from the entirety of Norway. It would be really interesting to study the potential for these data sources, how to integrate it in the analysis and find out what are the most relevant pieces of information.
