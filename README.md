
# NORWAY GOUND MOTION SERVICE

The Norway InSAR service offers ground motion data for the whole of Norway. Access [here](https://insar.ngu.no/).

Some information about the dataset can be found [here](https://www.ngu.no/en/topic/about-mapping-service).

You can download the data using the API [here](https://insar.ngu.no/api-docs/).
There is an example code of how to use it there. In this repo, the script `download_data.py` download the data.

Example usage:

`python3 download_data.py --dataset s1-asc1-v2020 --bbox=20.1404,69.3438,20.1827,69.3293 --path ./tmp/`

For a full description of the flags and download option, visit the API page above.

The downloaded data is a timeseries of ground motion with the parameters listed [here](https://www.ngu.no/en/topic/description-parameters).

## Precipitation data

### seNorge_2018

There 1km rainfall data for the whole of Norway from 1957 up to 2019.

seNorge_2018, daily precipitation, and temperature datasets over Norway, Cristian Lussana, Ole Einar Tveito, Andreas Dobler, and Ketil Tunheim. Earth Syst. Sci. Data, 11, 1531–1551, 2019.

Data is free to access [here](https://zenodo.org/record/3923703).

Paper [here](https://essd.copernicus.org/articles/11/1531/2019/).

### NASA GPM Data
It is possible to complement this ground motion data with the precipitation data from NASA GPM mission.
This data has been collected at regular intervals and can be downloaded for 30min, day and month intervals.
This data has coarser resolution than the ground motion data.

To download the precipitation data you can use the [package](https://pypi.org/project/gpm-precipitation-tools/) `gpm_precipitation_tools`. Documentation [here](https://gpm-precipitation-tools.readthedocs.io/en/latest/).

## Other datasets

Some other data that could be relevant (to download this data, you will need an account [here](https://www.geonorge.no/). This is mostly
in Norwegian, so might need some translating help):


* Bedrock 1:50000

* INSPIRE Transport network Road

* Height DTM 10

* Landslide/debris flow susceptibility
