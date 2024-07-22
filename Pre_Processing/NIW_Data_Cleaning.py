### National Inventory of Wetlands Data cleaning
## Adam Gallaher
## Cornell University
## 10-4-23

import arcpy
from arcpy import env

arcpy.env.parallelProcessingFactor = "75%"

#Setup
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r" " # results folder from FPV_NID_Preprocessing.py


wetland_FC = ['WV_Wetlands', 'VT_Wetlands', 'VA_Wetlands', 'RI_Wetlands',
              'PA_Wetlands', 'NY_Wetlands', 'NH_Wetlands', 'ME_Wetlands',
              'MD_Wetlands', 'MA_Wetlands', 'DE_Wetlands', 'CT_Wetlands', 'NJ_Wetlands',
              'DC_Wetlands']

proj = 'proj'
State_List = ([s.replace('_Wetlands', "") for s in wetland_FC])
Merge_List = []
print(State_List)
i = 0 
for infc in wetland_FC:
    print(infc)
    arcpy.management.Project(infc, infc + f'_{proj}', '102004')
    state = f"'{State_List[i]}'"
    print(state)
    Study_area = 'Northeast_Final'
    selection = arcpy.management.SelectLayerByAttribute(Study_area, 'NEW_SELECTION', 'STATE_ABBR = ' + state)
    i += 1
    result = arcpy.management.GetCount(selection)
    print(result)
    outFC = infc + "_clip"
    Merge_List.append(outFC)
    arcpy.analysis.PairwiseClip(infc, selection, outFC)
    
mergeFC = 'Northeast_Wetlands'
arcpy.management.Merge(Merge_List, mergeFC)
field = "WETLAND_TYPE"
values = ["Lake", "Freshwater Pond"]
query = "{0} IN {1}".format(arcpy.AddFieldDelimiters(mergeFC, field), tuple(values))

Wetland_filter = arcpy.SelectLayerByAttribute_management(mergeFC, "NEW_SELECTION", query)
print(arcpy.management.GetCount(Wetland_filter))
arcpy.DeleteFeatures_management(Wetland_filter)
