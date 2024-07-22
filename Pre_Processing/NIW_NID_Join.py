### National Hydrography Dataset/National Inventory of Dams Merge
## Adam Gallaher
## Cornell University
## 10-5-23

import arcpy
from arcpy import env

arcpy.env.parallelProcessingFactor = "100%"

#Setup
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r" " ## setup workspace

NHD_FC = 'Northeast_NHD_proj'
NID_FC = 'Northeast_NID_proj'
NID_Copy = 'Northeast_NID_near'
NHD_Copy = 'Northeast_NHD_Copy'

## Calculate area of NHD waterbodies
arcpy.AddField_management(NHD_FC, "Acres", "DOUBLE")
arcpy.management.CalculateGeometryAttributes(NHD_FC, [["Acres", "AREA_GEODESIC"]], "", "ACRES_US")
NHD_Records_orginal = arcpy.management.GetCount(NHD_FC)
print(NHD_Records_orginal)

## make copy of NHD/NID features to preserv orginal
arcpy.management.CopyFeatures(NHD_FC, NHD_Copy)
arcpy.management.CopyFeatures(NID_FC, NID_Copy)


## decode NHD waterbody type
arcpy.management.AddField(NHD_Copy, "FType_txt", "TEXT")
arcpy.management.AddField(NHD_Copy, "FCode_txt", "TEXT")

## update FType_txt field based on values in FType field
fields_type = ["FType", "FType_txt"]
with arcpy.da.UpdateCursor(NHD_Copy, fields_type) as cursor:
    for row in cursor:
        if row[0] == 493:
            row[1] = "Estuary"
        elif row[0] == 378:
            row[1] = "Ice Mass"
        elif row[0] == 390:
            row[1] = "Lake/Pond"
        elif row[0] == 361:
            row[1] = "Playa"
        elif row[0] == 436:
            row[1] = "Reservoir"
        elif row[0] == 466:
            row[1] = "Swamp/Marsh"
        cursor.updateRow(row)
del row
del cursor

## update FCode_txt field based on values in FCode field
fields_code = ["FCode", "FCode_txt"]
with arcpy.da.UpdateCursor(NHD_Copy, fields_code) as cursor:
    for row in cursor:
        if row[0] == 49300:
            row[1] = "Estuary"
        elif row[0] == 37800:
            row[1] = "Ice Mass"
        elif row[0] == 39000:
            row[1] = "Lake/Pond"
        elif row[0] == 39001:
            row[1] = "Lake/Pond Intermittent"
        elif row[0] == 39004:
            row[1] = "Lake/Pond Perennial"
        elif row[0] == 39005:
            row[1] = "Lake/Pond Intermittent High"
        elif row[0] == 39006:
            row[1] = "Lake/Pond Intermittent Photo"
        elif row[0] == 39009:
            row[1] = "Lake/Pond Perennial Avg"
        elif row[0] == 39010:
            row[1] = "Lake/Pond Perennial Pool"
        elif row[0] == 39011:
            row[1] = "Lake/Pond Perennial Photo"
        elif row[0] == 39012:
            row[1] = "Lake/Pond Perennial Spillway"
        elif row[0] == 36100:
            row[1] = "Playa"
        elif row[0] == 43600:
            row[1] = "Reservoir"
        elif row[0] == 43601:
            row[1] = "Reservoir Aquaculture"
        elif row[0] == 43603:
            row[1] = "Reservoir Pool"
        elif row[0] == 43604:
            row[1] = "Reservoir tailings"
        elif row[0] == 43605:
            row[1] = "Reservoir tailings"
        elif row[0] == 43606:
            row[1] = "Reservoir disposal"
        elif row[0] == 43607:
            row[1] = "Reservoir evaporator"
        elif row[0] == 43608:
            row[1] = "Reservoir swimming"
        elif row[0] == 43609:
            row[1] = "Reservoir cooling pond"
        elif row[0] == 43610:
            row[1] = "Reservoir filtration"
        elif row[0] == 43611:
            row[1] = "Reservoir settling"
        elif row[0] == 43612:
            row[1] = "Reservoir sewage"
        elif row[0] == 43613:
            row[1] = "Reservoir storage"
        elif row[0] == 43614:
            row[1] = "Reservoir storage inter"
        elif row[0] == 43615:
            row[1] = "Reservoir storage perennial"
        elif row[0] == 43617:
            row[1] = "Reservoir storage"
        elif row[0] == 43618:
            row[1] = "Reservoir unspecified"
        elif row[0] == 43619:
            row[1] = "Reservoir unspecified"
        elif row[0] == 43621:
            row[1] = "Reservoir storage"
        elif row[0] == 43623:
            row[1] = "Reservoir evaporator"
        elif row[0] == 43624:
            row[1] = "Reservoir treatment"
        elif row[0] == 43625:
            row[1] = "Reservoir disposal"
        elif row[0] == 43626:
            row[1] = "Reservoir disposal"
        elif row[0] == 46600:
            row[1] = "Swamp/Marsh"
        elif row[0] == 46601:
            row[1] = "Swamp/Marsh inter"
        elif row[0] == 46602:
            row[1] = "Swamp/Marsh Perennial"
        cursor.updateRow(row)
del row
del cursor

## delete any waterbodies smaller then 1 acre
query = 'Acres < 2.5'
one_acre = arcpy.SelectLayerByAttribute_management(NHD_Copy, "NEW_SELECTION", query) 
arcpy.management.DeleteFeatures(one_acre)
query = "\"FType_txt\" IN ('Swamp/Marsh', 'Estuary', 'Playa')"
unsuitable_water = arcpy.SelectLayerByAttribute_management(NHD_Copy, "NEW_SELECTION", query)
arcpy.management.DeleteFeatures(unsuitable_water)


## run a near analysis to find all matching NID dams to NHD waterbodies
NHD_Records = arcpy.management.GetCount(NHD_Copy)
print(NHD_Records)

arcpy.analysis.Near(NID_Copy, NHD_Copy, "", "LOCATION", "", "GEODESIC", "", "Miles")
## delete unmatched dams
query2 = 'NEAR_DIST > 0.06'
NHD_NID_Delete = arcpy.SelectLayerByAttribute_management(NID_Copy, "NEW_SELECTION", query2)
arcpy.management.DeleteFeatures(NHD_NID_Delete)

## join new NID with NHD features
NHD_NID_Join = arcpy.management.AddJoin(NHD_Copy, "NID_Join", NHD_NID_Delete, "NEAR_FID", "KEEP_ALL")

NHD_NID_Records = arcpy.management.GetCount(NHD_NID_Join)
print(NHD_NID_Records)
## Copy joined features to new FC
outLocation = r" " ## setup output location
arcpy.FeatureClassToFeatureClass_conversion(NHD_NID_Join, outLocation, "Northeast_NHD_NID")


## Identify duplicate records
Northeast_NHD_NID = 'Northeast_NHD_NID'

query3 = 'NEAR_FID IS NOT NULL'
identical = arcpy.SelectLayerByAttribute_management(Northeast_NHD_NID, "NEW_SELECTION", query3)
arcpy.DeleteIdentical_management(identical, "NEAR_FID")


## Join NHD Northeast waterbodies with TNC Lakes and Ponds dataset
OutFC_Join = 'Northeast_TNC_Final'
join_FC = 'TNC_Lakes_Ponds_proj'
arcpy.analysis.SpatialJoin(Northeast_NHD_NID, join_FC, OutFC_Join, "", "KEEP_ALL", "", "COMPLETELY_CONTAINS")


## Identify waterbodies within 1 mile of interconnection point (transmission line or substation)
transmission = 'Northeast_Transmission_Buffer_1mi_proj'

intersection = arcpy.management.SelectLayerByLocation(OutFC_Join, "INTERSECT", transmission, "", "NEW_SELECTION")
arcpy.management.CopyFeatures(intersection, 'Northeast_Selection_1')

## Identify waterbodies wholly within 1 mile of interconnection point (transmission line or substation)
intersection_b = arcpy.management.SelectLayerByLocation(OutFC_Join, "COMPLETELY_WITHIN", transmission, "", "NEW_SELECTION")
arcpy.management.CopyFeatures(intersection_b, 'Northeast_Selection_1b')

## identify if above selected waterbodies intersect a local road
local_roadsDB = ' '  ## local roads
local_roadsFC = local_roadsDB + 'Northeast_local_roads'


roads_check = arcpy.management.SelectLayerByLocation('Northeast_Selection_1', "WITHIN_A_DISTANCE", local_roadsFC, "0.5 Miles", "NEW_SELECTION")
arcpy.management.CopyFeatures(roads_check, 'Northeast_Selection_2')

## identify if selected waterbodies (within) intersect a local road
roads_check_b = arcpy.management.SelectLayerByLocation('Northeast_Selection_1b', "WITHIN_A_DISTANCE", local_roadsFC, "0.5 Miles", "NEW_SELECTION")
arcpy.management.CopyFeatures(roads_check_b, 'Northeast_Selection_2b')
