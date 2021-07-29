import requests
import os
import haversine as hs
import pandas as pd 
import numpy as np
import folium
from folium.plugins import HeatMapWithTime
import pickle
### Function imports 
from user_inputs import user_lat_lon_address,hs_distance,get_LSOA_city_region
from mapping import heat_map, heat_map_time
from gata_data import get_lsoa_data
raw_data_filepath = '../raw_data/'

def create_area_df(force):
    infile = open(f'{raw_data_filepath}lsoa_data.pkl','rb')
    lsoa_df = pickle.load(infile)
    lsoa_df = lsoa_df[['force','file_name']].drop_duplicates()
    lsoa_df = lsoa_df.reset_index()
    indx = lsoa_df[lsoa_df['force']==force].index.values[0]
    file_name = lsoa_df.iloc[indx]['file_name']
    area_path = raw_data_filepath+file_name+'.pkl'
    area_df = pd.read_pickle(area_path)
    return area_df

raw_data_filepath = '../raw_data/'
u_lat, u_lon, u_full_add = user_lat_lon_address("Old Trafford")
lsoa_df = get_lsoa_data()
df, lsoa, city, region = get_LSOA_city_region(lsoa_df,u_lon,u_lat)
area_df = create_area_df(region)
#heat_map(area_df,u_lat,u_lon,user_address=u_full_add,radius = 2, crime="Anti-social behaviour")
heat_map_time(area_df,u_lat,u_lon,user_address=u_full_add,radius = 2, crime="Anti-social behaviour")



