
import streamlit as st
import pandas as pd
from projectUKcrime.gata_data import get_lsoa_data, create_area_df
from projectUKcrime.user_inputs import user_lat_lon_address, get_LSOA_city_region
from projectUKcrime.mapping import heat_map, heat_map_time
from projectUKcrime.plotting import plot_relative_crime_rate,get_crime_type_rate
import folium
from streamlit_folium import folium_static

pu = False



# title
#st.title('UK crime radar')
#st.set_page_config(layout="wide")

#user inputs
with st.form(key="my_form"):
   
   user_add = st.sidebar.text_input(label = 'Please enter an address in England?')
   map_type = st.sidebar.selectbox('Select heat map type',('Static', 'Moving'))
   u_radius = st.sidebar.selectbox(
   'Please choose an area size for displaying crime data?',
   ('1', '5', '10','50'))
   crime_type = st.sidebar.selectbox(
   'Please choose a crime type?',
   ('Anti-social behaviour',
   'Bicycle theft',
   'Burglary',
   'Criminal damage and arson',
   'Drugs',
   'Other theft',
   'Possession of weapons',
   'Public order',
   'Robbery',
   'Shoplifting',
   'Theft from the person',
   'Vehicle crime',
   'Violence and sexual offences'))
   submit_button = st.form_submit_button(label="Submit")
if submit_button:
   st.write("Generating your data")


#get user location and full address
u_lat, u_lon, u_full_add = user_lat_lon_address(user_add)
lsoa_df = get_lsoa_data()
df, lsoa, city, region = get_LSOA_city_region(lsoa_df,u_lon,u_lat)
area_df = create_area_df(region)
u_radius = float(u_radius)

#user if prompt to verify his/her full address
#st.sidebar.write(f"Please verify your full address & re-type as need be:\n {u_full_add}")

#User select data granularity
#pu_option = st.sidebar.selectbox(
 #"Select how granular you want your data to be?",
 #('LSOA', 'City', 'Police Force'))


if map_type == "Static":
   base_map = heat_map(area_df,u_lat,u_lon,user_address=u_full_add,radius = u_radius, crime = crime_type)
else:
   base_map = heat_map_time(area_df,u_lat,u_lon,user_address=u_full_add,radius = u_radius, crime = crime_type)
crime_plot = plot_relative_crime_rate(area_df,city,crime_type)
crime_table_display = get_crime_type_rate(area_df,city=city,district=lsoa)
#load the LSOA data to identify user LSOA, City, Force
#lsoa_df = get_lsoa_data()
#u_lsoa_df, u_lsoa, u_city, u_force = get_LSOA_city_region(lsoa_df,u_lon,u_lat)
#if user_add == None:
   # st.write(u_lsoa_df, u_lsoa, u_city, u_force)
#get the datafram for user_force

if user_add:
   folium_static(base_map)
   st.pyplot(crime_plot)
   st.write(crime_table_display)
