
import streamlit as st
import pandas as pd
from projectUKcrime.gata_data import get_lsoa_data, create_area_df
from projectUKcrime.user_inputs import user_lat_lon_address, get_LSOA_city_region
from projectUKcrime.mapping import heat_map
import folium
from streamlit_folium import folium_static

pu = False



# after this is done, run 
# streamlit run app.py


# title
st.title('UK crime radar')
#st.set_page_config(layout="wide")

# User enters his/her address
user_add = st.sidebar.text_input(label = 'Please key in your address in the UK?')

#get user location and full address
u_lat, u_lon, u_full_add = user_lat_lon_address(user_add)
lsoa_df = get_lsoa_data()
df, lsoa, city, region = get_LSOA_city_region(lsoa_df,u_lon,u_lat)
area_df = create_area_df(region)
base_map = heat_map(area_df,u_lat,u_lon,user_address=u_full_add,radius = 1, crime="Bicycle theft")

#user if prompt to verify his/her full address
st.sidebar.write(f"Please verify your full address & re-type as need be:\n {u_full_add}")

#User select data granularity
pu_option = st.sidebar.selectbox(
 "Select how granular you want your data to be?",
 ('LSOA', 'City', 'Police Force'))
u_radius = st.sidebar.selectbox(
 'Kindly choose a radius around your address in km?',
 ('1', '5', '10','50'))
u_radius = float(u_radius)

base_map = heat_map(area_df,u_lat,u_lon,user_address=u_full_add,radius = u_radius, crime="Bicycle theft")


#load the LSOA data to identify user LSOA, City, Force
#lsoa_df = get_lsoa_data()
#u_lsoa_df, u_lsoa, u_city, u_force = get_LSOA_city_region(lsoa_df,u_lon,u_lat)
#if user_add == None:
   # st.write(u_lsoa_df, u_lsoa, u_city, u_force)
#get the datafram for user_force


#get the 

# map
folium_static(base_map)

