import os
import csv
import pandas as pd
import PySAM.ResourceTools as tools
import PySAM.Pvwattsv8 as pv


# --- Initialize Solar Resource Fetcher with minimum parameters ---
nsrdbfetcher = tools.FetchResourceFiles(
                tech='solar',
                nrel_api_key=' ',  ## your NREL API key
                nrel_api_email=' ', ## the email used to obtain API key
                resource_dir=' ', ## path to store weather files
                workers=1)


## get weather files in list to check for duplicats
kW_filename = open(' ' ## path to folder containing location and unique ID for each location in study (e.g., waterbodies)
                   '/ ', 'r') ## file name
file = csv.DictReader(kW_filename)
weather_files = []

for col in file:
    weather_files.append(col['weather_files'])
lst = []

for index, item in enumerate(weather_files):

    path = (" " ## path to store new weather files
            "/ /%s") % weather_files[index] ## folder for new weather files
    isExist = os.path.exists(path)
    if not isExist:
        print(f"Downloading Weather File: {path}")
        df = pd.read_csv(
            " " ## path to folder containing location and unique ID for each location in study (e.g., waterbodies) 
            "/ ") ## filename

        x = (df.iloc[index]['weather_lon'])
        y = (df.iloc[index]['weather_lat'])
        lst_tuple = (x, y)
        lst.append(lst_tuple)


## list of (lon, lat) tuples or shepely points
#lon_lats = lst_tuple
lon_lats = lst
nsrdbfetcher.fetch(lon_lats)

## Get resource data file path
nsrdb_path_dict = nsrdbfetcher.resource_file_paths_dict
nsrdb_fp = nsrdb_path_dict[lon_lats[0]]
