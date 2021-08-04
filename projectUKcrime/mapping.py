import pandas as pd 
import numpy as np
import folium
from folium.plugins import HeatMapWithTime
import haversine as hs
from projectUKcrime.user_inputs import hs_distance



## crime is now a list to enable filtering by multiple crimes
def heat_map(area_df,u_lat,u_long,user_address,radius = None, city = None, crime_list = "All"):
    area_df['distance'] = area_df[['Longitude','Latitude']].apply(lambda x: hs_distance(x[1], x[0], lat2=u_lat, long2=u_long),axis=1)
    if city != None: 
        area_df = area_df[area_df["LSOA name"].str.contains(city)]
    if radius!= None:
        area_df = area_df[area_df["distance"]<= radius]
    if crime_list != "All":
        area_df = area_df[area_df["Crime type"] == crime_list]
    if radius == 1: 
        zoom = 15
    elif radius == 5: 
        zoom = 13
    elif radius == 10:
        zoom = 12.5
    elif radius == 50:
        zoom = 9
    
    
    map_centre = (u_lat,u_long)
    base_map = folium.Map(location=map_centre, zoom_start=zoom,width=800,height=700,title=None)
    folium.Marker(location=(u_lat,u_long),popup=user_address).add_to(base_map)
    for crime in crime_list: 
        area_df_ = area_df[area_df["Crime type"]== crime]
        lat_list = area_df_['Latitude'].tolist()
        long_list = area_df_['Longitude'].tolist()
        individual_crime_coordinates = set(zip(lat_list,long_list))
        layer = folium.plugins.HeatMap(individual_crime_coordinates,overlay=True,min_opacity=0.1,show=False)
        layer.layer_name = f"{crime}"
        base_map.add_child(layer)
    folium.LayerControl(position='topright',collapsed=False).add_to(base_map)   
    return base_map

    

def heat_map_time(area_df,u_lat,u_long,user_address,radius = None, city = None, crime=None):
    area_df['distance'] = area_df[['Longitude','Latitude']].apply(lambda x: hs_distance(x[1], x[0], lat2=u_lat, long2=u_long),axis=1)
    if crime != None:
        area_df = area_df[area_df["Crime type"] == crime]
    if radius!= None:
        area_df = area_df[area_df["distance"]<= radius]
    if city != None: 
        area_df = area_df[area_df["LSOA name"].str.contains(city)]
    if radius == 1: 
        zoom = 15
    elif radius == 5: 
        zoom = 13
    elif radius == 10:
        zoom = 12.5
    elif radius == 50:
        zoom = 9
    
    
    
    date_index = list(area_df['Month'].sort_values().unique())
    area_df["Time"] = area_df["Month"].map(lambda x:x.replace('-',''))
    area_df["Time"] = area_df["Time"].map(lambda x:int(x))
    area_df = area_df[["Longitude","Latitude","Time"]]
    area_df = area_df.dropna()
    date_list = list(area_df["Time"].unique())
    lat_long_list = []
    for i in date_list:
        temp=[]
        for index,instance in area_df[area_df['Time'] == i].iterrows():
            temp.append([instance['Latitude'],instance['Longitude']])
        lat_long_list.append(temp)
    map_centre = (u_lat,u_long)
    base_map = folium.Map(location=map_centre, zoom_start=zoom,width=800,height=700,title=None)
    folium.Marker(location=(u_lat,u_long),popup=user_address).add_to(base_map)
    HeatMapWithTime(lat_long_list,auto_play=False,position='bottomright',min_opacity=0.1,index=date_index,max_speed=1).add_to(base_map)
    return base_map
 

