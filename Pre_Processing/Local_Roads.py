### US DOT local roads extraction
## Adam Gallaher
## Cornell University
## 10-5-23

import arcpy
import re
from arcpy import env

arcpy.env.parallelProcessingFactor = "100%"

arcpy.env.overwriteOutput = True
arcpy.env.workspace = r" " ## folder with local roads GIS data

InputDB = " " ## file with boundy of study area
field_name = "FIPS"

Feature_ID = []
with arcpy.da.SearchCursor(InputDB, field_name) as cursor:
    for row in cursor:
        Feature_ID.append(row[0])
        
State_Names = ["Virginia", "Pennsylvania", "New York", "West Virginia", "Maryland",
               "New Jersey", "Maine", "Massachusetts", "Vermont", "New Hampshire",
               "Connecticut", "Rhode Island", "Delaware", "District of Columbia"]


Local_Roads = 'USA_Local_Roads'
print(Local_Roads)
FeatureClasses = []
i = 0
for values in Feature_ID:
    record = f"'{Feature_ID[i]}'"
    print(record)
    selection = arcpy.SelectLayerByAttribute_management(InputDB, "NEW_SELECTION", 'FIPS = ' + record)
    result = arcpy.management.GetCount(selection)
    print(result)
  
    test = arcpy.ValidateFieldName(record)
    print(test)
    outPutFC = " " + test ## output folder to save processed data
    print(outPutFC)
    FeatureClasses.append(outPutFC)
    arcpy.analysis.PairwiseClip(Local_Roads, selection, outPutFC)
    i += 1

mergeFC = 'Northeast_local_Roads'
arcpy.management.Merge(FeatureClasses, mergeFC)
