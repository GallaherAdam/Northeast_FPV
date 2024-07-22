### National Inventory of Dams data cleaning and geographic subsetting
### Adam Gallaher, Ph.D.
### Cornell University

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import arcpy

## Read in raw data
WD = " " ## set working directory with NID data
Data = WD + "/NID_Raw.csv"
print(Data)

## Convert csv file into pandas dataframe using Federal ID as index
rawdata = pd.read_csv(Data, index_col = "Federal_ID")
df = pd.DataFrame(rawdata)
df = df.dropna(axis=0, subset=['Primary Purpose'])

## Subset data to specifc state (e.g., New York)
state_list = ['Maine', 'New Hampshire', 'Vermont', 'New York', 'Massachusetts', 'Rhode Island', 'Connecticut',
              'New Jersey', 'Pennsylvania', 'Delaware', 'Maryland', 'West Virginia', 'Virginia', 'District of Columbia']
#NYS_Dams = df[df["State"] == "New York"]
NYS_Dams = df[df["State"].isin(state_list)]

## Subset data to specific columns
NYS_Dams_Data = NYS_Dams[["NID ID", "Latitude", "Longitude", "State", "County",
                            "Primary Owner Type","Primary Purpose", "Purposes",
                            "Primary Dam Type", "Year Completed",
                            "Hazard Potential Classification", "Condition Assessment"]]

NYS_Dams_Rename = NYS_Dams_Data.rename(columns={'NID ID': 'NID_ID', 'Primary Owner Type': 'Primary_Owner',
                        'Primary Purpose': 'Primary_Purpose', 'Primary Dam Type': 'Primary_Dam_Type',
                        'Year Completed': 'Year_Completed',
                        'Hazard Potential Classification': 'Hazard_Class',
                        'Condition Assessment': 'Condition'})

new_columns = list(NYS_Dams_Rename)
print(new_columns)
NYS_Dams_Rename.Primary_Purpose.unique()

## Save subset to csv for GIS
NYS_Dams_Rename.to_csv(WD + "/Northeast_NID.csv", index=False)

## Set GIS WD
arcpy.env.workspace = r" " ## set file geodatabase for results

## Add Lat and Long to new GIS point file
in_data = WD + "/Northeast_NID.csv"
NYS_NID_Pts = "Northeast_NID_Raw"
x_coords = "Longitude"
y_coords = "Latitude"
arcpy.management.XYTableToPoint(in_data, NYS_NID_Pts, "Longitude", "Latitude",
                                "", arcpy.SpatialReference(4326))

## Project data to NAD 1983 UTM Zone 18N(26918)
NYS_NID_Proj = "Northeast_NID_Proj"
arcpy.management.Project(NYS_NID_Pts, NYS_NID_Proj, arcpy.SpatialReference(26918),
                         "WGS_1984_(ITRF00)_To_NAD_1983")
