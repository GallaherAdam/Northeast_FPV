import json
import PySAM.Pvwattsv8 as pv
import pandas as pd
import csv

kW_filename = open(' ' ## csv folder containing the latitude and longitude of the location of interest (e.g., waterbodies)
                   '/ ', 'r') ## file name
file = csv.DictReader(kW_filename)
Kw_list = []
FPV_ID = []
weather_files = []
Annual_Energy_Output = []
Lat = []
Long = []

i = 0
for col in file:
    Kw_list.append(col['fpv_system_size_kw'])
    FPV_ID.append(col['fpv_id'])
    weather_files.append(col['weather_files'])
    Lat.append(col['water_lat'])
    Long.append(col['water_lon'])

## Creating a new instance of the Pvwatts 8 module to run
system_model = pv.new()

## gathering inputs from the pre-configured JSON file
with open(' ', 'r') as f: ## a JSON file pre-configured from SAM
    pv_inputs = json.load(f)

## iterate through the input key-value pairs and set the module inputs
for k, v in pv_inputs.items():
    if k != 'number_inputs':
        system_model.value(k, v)

for k in Kw_list:
    weather_path = (" " ## path to folder containing the weather files corresponding to each geographic location (e.g., waterbodies)
                    "/ ") % weather_files[i] ## eather file
    print(weather_path)
    print("these are the weather file: %s" % weather_files[i])
    system_model.SolarResource.solar_resource_file = weather_path

    capacity = float(Kw_list[i])  # kWdc
    system_model.SystemDesign.system_capacity = capacity
    print("this is the system capacity: %s" % Kw_list[i])
    i = i + 1
    print(i)

    system_model.execute()

    annual_energy = system_model.Outputs.ac_annual
    Annual_Energy_Output.append(annual_energy)

dictionary = {'fpv_id': FPV_ID, 'water_lat': Lat, 'water_lon': Long, 'Year1_Energy_kWh': Annual_Energy_Output,
              'weather_files': weather_files, 'System_Size_kW': Kw_list}
dataframe = pd.DataFrame(dictionary)
dataframe.to_csv(' '  ## output folder 
                 '/ ') ## output file
