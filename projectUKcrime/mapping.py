import pandas as pd 
import numpy as np
import os
import glob
import folium
import folium.plugins
import datetime
from folium.plugins import HeatMapWithTime
import statistics
import requests


def heat_map(crime_type,area):
    crime_type = crime_type.capitalize()
    area_df = create_area_df(area)
    individual_crime_df = area_df[area_df["Crime type"]==crime_type][['Longitude','Latitude']]
    individual_crime_df=individual_crime_df.dropna()
    lat_list = individual_crime_df['Latitude'].tolist()
    long_list = individual_crime_df['Longitude'].tolist()
    individual_crime_coordinates = set(zip(lat_list,long_list))
    map_centre = (statistics.mean(lat_list), statistics.mean(long_list))
    base_map = folium.Map(location=map_centre, zoom_start=10)
    
    title_html = '''
             <h3 align="center" style="font-size:20px"><b>{title} in {location} from 6/2018 to 5/2021</b></h3>
             '''.format(title=crime_type.title(),location=area.title())
    base_map.get_root().html.add_child(folium.Element(title_html))
    
                                       
    folium.plugins.HeatMap(individual_crime_coordinates,overlay=True,min_opacity=0.01).add_to(base_map)
    display(base_map)

def heat_map_time(crime_type,area):
    crime_type = crime_type.capitalize()
    area_df = create_area_df(area)
    crime_area_df= area_df[area_df["Crime type"]==crime_type][['Longitude','Latitude','Month']]
    date_index = list(crime_area_df['Month'].sort_values().unique())
    crime_area_df["Time"] = crime_area_df["Month"].map(lambda x:x.replace('-',''))
    crime_area_df["Time"] = crime_area_df["Time"].map(lambda x:int(x))
    crime_area_df = crime_area_df[["Longitude","Latitude","Time"]]
    crime_area_df = crime_area_df.dropna()
    date_list = list(crime_area_df["Time"].unique())
    
   
    lat_long_list = []
    for i in date_list:
        temp=[]
        for index,instance in crime_area_df[crime_area_df['Time'] == i].iterrows():
            temp.append([instance['Latitude'],instance['Longitude']])
        lat_long_list.append(temp)
    
    map_centre = (statistics.mean(crime_area_df['Latitude'].tolist()),statistics.mean(crime_area_df['Longitude'].tolist()))
    base_map = folium.Map(location=map_centre, zoom_start=10)
    HeatMapWithTime(lat_long_list,auto_play=True,position='bottomright',min_opacity=0.1,index=date_index).add_to(base_map)
    display(base_map)
    