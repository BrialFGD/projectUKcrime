import streamlit as st
import pandas as pd
import requests
from gata_data import get_lsoa_data
from user_inputs import user_lat_lon_address, get_lsoa_city_region

pu = False

# title
st.title('UK crime radar')

# User enters his/her address
user_add = st.sidebar.text_input(label = 'Please key in your address in the UK?')

#get user location and full address
u_lat, u_lon, u_full_add = user_lat_lon_address(user_add)

#user if prompt to verify his/her full address
st.sidebar.write(f"Please verify your full address & re-type as need be:\n {u_full_add}")

#User select data granularity
pu_option = st.sidebar.selectbox(
...     "Select how granular you want your data to be?',
...     ('LSOA', 'City', 'Police Force'))
radius = st.sidebar.selectbox(
...     '**FOR V2** Kindly choose a radius around your address in km?',
...     ('1', '5', '10','50'))

#load the LSOA data to identify user LSOA, City, Force
lsoa_df = get_lsoa_data()
u_lsoa_df, u_lsoa, u_city, u_force = get_lsoa_city_region(lsoa_df,u_lon,u_lat)

#get the datafram for user_force


#get the 

# map
st.map(pd.DataFrame({'lat': [pu_lat], 'lon': [pu_lon]}))

