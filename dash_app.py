# -*- coding: utf-8 -*-
"""
This script prompts the user for a given land cover/s and will proceed to compute the percentage of adults that nest on the given land cover/s in Northampton County on the Virginia Barrier Islands.
Script written by Alden Summerville
"""

import arcpy
from sys import argv
from dash import Dash, dcc, html, Input, Output, State # for dash app

# instantiate dash object
app = Dash(__name__)

# to include markdown
markdown_text = "Enter a land cover type or type 'all' to calculate all layers (Bare_Land/Sand, Forest/Shrub, Planted_Crop/Grassland, Salt_Marsh, Water): "

app.layout = html.Div(children=[
    html.H1(children='GIS Analysis Web App'),

    html.Div(children='''
        Objective: Percentage of adults that nest on a given land cover/s in Northampton County on the Virginia Barrier Islands
    '''),

    dcc.Markdown(children=markdown_text),

    html.Div(dcc.Input(id='input-on-submit', type='text')),
    html.Button('Analyze', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children='Enter a land cover and press Analyze')
             
])

# GIS analysis fxn
@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', "n_clicks"),
    State('input-on-submit', 'value')
)
def main(n_clicks, value):
    
    print("This script prompts the user for a given land cover/s and will proceed to compute the percentage of adults that nest on the given land cover/s in Northampton County on the Virginia Barrier Islands")
    print('Script written by Alden Summerville')
    
    # user input
    input_list = ['Bare_Land/Sand', 'Forest/Shrub', 'Planted_Crop/Grassland', 'Salt_Marsh', 'Water', 'all']
    lc_list = ['Bare_Land/Sand', 'Forest/Shrub', 'Planted_Crop/Grassland', 'Salt_Marsh', 'Water']

    # exp = input("Enter a land cover type or type 'all' to calculate all layers (Bare_Land/Sand, Forest/Shrub, Planted_Crop/Grassland, Salt_Marsh, Water): ")
    exp = value

    while exp not in input_list:
        return "Incorrect input. Please enter one of: Bare_Land/Sand, Forest/Shrub, Planted_Crop/Grassland, Salt_Marsh, Water, all"

    # with arcpy.EnvManager(scratchWorkspace=r"C:\Users\Alden Summerville\MEGASync\Documents\AdvGIS\Assignment1-birds\Assignment1-birds\Assignment1-birds.gdb", workspace=r"C:\Users\Alden Summerville\MEGASync\Documents\AdvGIS\Assignment1-birds\Assignment1-birds\Assignment1-birds.gdb"):
    #     Model(exp)
    Model(exp)


def Model(exp):  # Model used to have as input: Expression="LANDCOVER = 'Bare_Land/Sand'"

    # ***Something with dash incorrectly passing the features through the analysis fxns...
    # at a certain point, give up / just change the incorrect input to one of the result outputs lol...kinda cheap tho

    wspace = r"C:\Users\Alden Summerville\MEGASync\Documents\AdvGIS\Assignment1-birds\Assignment1-birds\Assignment1-birds.gdb"

    if exp != 'all':
        Expression = "LANDCOVER = '" + str(exp) + "'"

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    birds = wspace + r"\birds"
    Land_cover = wspace + r"\Land_cover"

    print('Analyzing...')

    # Process: Intersect (Intersect) 
    Output_Feature_Class = "C:\\Users\\Alden Summerville\\MEGASync\\Documents\\AdvGIS\\Assignment1-birds\\Assignment1-birds\\Assignment1-birds.gdb\\birds_Intersect"
    arcpy.Intersect_analysis(in_features=[[birds, ""], [Land_cover, ""]], out_feature_class=Output_Feature_Class, join_attributes="ALL", cluster_tolerance="", output_type="INPUT")

    # Process: Summary Statistics (Summary Statistics) 
    total_adults = "C:\\Users\\Alden Summerville\\MEGASync\\Documents\\AdvGIS\\Assignment1-birds\\Assignment1-birds\\Assignment1-birds.gdb\\total_adults"
    arcpy.Statistics_analysis(in_table=Output_Feature_Class, out_table=total_adults, statistics_fields=[["ADULTS", "SUM"]], case_field=[])

    # Process: Summary Statistics (2) (Summary Statistics) 
    adults_by_landcover = "C:\\Users\\Alden Summerville\\MEGASync\\Documents\\AdvGIS\\Assignment1-birds\\Assignment1-birds\\Assignment1-birds.gdb\\adults_by_landcover"
    arcpy.Statistics_analysis(in_table=Output_Feature_Class, out_table=adults_by_landcover, statistics_fields=[["ADULTS", "SUM"]], case_field=["LANDCOVER"])

    # Process: Table Select (Table Select) 
    if exp != 'all':
        total_adults_landcover_select = f"C:\\Users\\Alden Summerville\\MEGASync\\Documents\\AdvGIS\\Assignment1-birds\\Assignment1-birds\\Assignment1-birds.gdb\\total_adults_landcover_{exp.replace('/', '_')}"
        arcpy.TableSelect_analysis(in_table=adults_by_landcover, out_table=total_adults_landcover_select, where_clause=Expression)
        
        #number of adults for desired layer  
        vals = []
        rows = arcpy.SearchCursor(total_adults_landcover_select)
        for row in rows:
            num = row.getValue('SUM_ADULTS')
            vals.append(num)

        #total adults value
        rows = arcpy.SearchCursor(total_adults)
        for row in rows:
            num = row.getValue('SUM_ADULTS')
            vals.append(num)

        #percentage
        p = round(vals[0]/vals[1]*100, 2)
        result = f'The percentage of adults on the {exp} land cover is {p} percent'
        return result

    else:
        for lc_type in lc_list:
            Expression = "LANDCOVER = '" + str(lc_type) + "'"
            total_adults_landcover_select = f"C:\\Users\\Alden Summerville\\MEGASync\\Documents\\AdvGIS\\Assignment1-birds\\Assignment1-birds\\Assignment1-birds.gdb\\total_adults_landcover_{lc_type.replace('/', '_')}"
            arcpy.TableSelect_analysis(in_table=adults_by_landcover, out_table=total_adults_landcover_select, where_clause=Expression)

            #number of adults for desired layer  
            vals = []
            rows = arcpy.SearchCursor(total_adults_landcover_select)
            for row in rows:
                num = row.getValue('SUM_ADULTS')
                vals.append(num)
            
            #total adults value
            rows = arcpy.SearchCursor(total_adults)
            for row in rows:
                num = row.getValue('SUM_ADULTS')
                vals.append(num)
            
            #percentage
            p = round(vals[0]/vals[1]*100, 2)
            print(f'The percentage of adults on the {lc_type} land cover is {p} percent')

    # delete features
    arcpy.management.Delete(wspace + "\birds_Intersect")

    print('Analysis complete')
    print('(you may view the output tables in the arcgis project if desired)')


# run analysis
# with arcpy.EnvManager(scratchWorkspace=r"C:\Users\Alden Summerville\MEGASync\Documents\AdvGIS\Assignment1-birds\Assignment1-birds\Assignment1-birds.gdb", workspace=r"C:\Users\Alden Summerville\MEGASync\Documents\AdvGIS\Assignment1-birds\Assignment1-birds\Assignment1-birds.gdb"):
#     Model(*argv[1:])

if __name__ == '__main__':
    app.run_server(debug=True)