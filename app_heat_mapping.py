import streamlit as st
import pandas as pd
from projectUKcrime.gata_data import get_lsoa_data, create_area_df
from projectUKcrime.user_inputs import user_lat_lon_address, get_LSOA_city_region,hs_distance
from projectUKcrime.mapping import heat_map, heat_map_time
import folium
from streamlit_folium import folium_static





def app():
    #st.title('UK crime heatmaps')

#user inputs
    with st.form(key="my_form"):
        with st.sidebar:
            user_add = st.sidebar.text_input(label = 'Please enter an address in England?')
            u_radius = st.sidebar.selectbox(
            'Please choose an area size for displaying crime data?',
            ('1', '5', '10','50'))

            crime_type_list = ['Anti-social behaviour',
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
            'Violence and sexual offences']
   
            crime_type = st.sidebar.multiselect("Please choose crime type(s):",crime_type_list)

            submit_button = st.form_submit_button(label="Submit")

            if submit_button:
                st.sidebar.write("Generating your data")


#get user location and full address
    u_lat, u_lon, u_full_add = user_lat_lon_address(user_add)
    lsoa_df = get_lsoa_data()
    df, lsoa, city, region = get_LSOA_city_region(lsoa_df,u_lon,u_lat)
    area_df = create_area_df(region)
    u_radius = float(u_radius)


    base_map = heat_map(area_df,u_lat,u_lon,user_address=u_full_add,radius = u_radius, crime_list = crime_type)
    


    if user_add:
        folium_static(base_map,width=800,height=700)
   
