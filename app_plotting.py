from projectUKcrime.plotting import plot_relative_crime_rate,get_crime_type_rate
import streamlit as st
import pandas as pd
from projectUKcrime.gata_data import get_lsoa_data, create_area_df
from projectUKcrime.user_inputs import user_lat_lon_address, get_LSOA_city_region,hs_distance





def app():
    #st.title('UK crime heatmaps')

#user inputs
    with st.form(key="my_form"):
        with st.sidebar:
            user_add = st.sidebar.text_input(label = 'Please enter an address in England?')

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
   
            crime_type = st.sidebar.selectbox("Plsease choose crime type:",crime_type_list)

            submit_button = st.form_submit_button(label="Submit")

            if submit_button:
                st.sidebar.write("Generating your data")


#get user location and full address
    u_lat, u_lon, u_full_add = user_lat_lon_address(user_add)
    lsoa_df = get_lsoa_data()
    df, lsoa, city, region = get_LSOA_city_region(lsoa_df,u_lon,u_lat)
    area_df = create_area_df(region)

    crime_plot = plot_relative_crime_rate(area_df,city,crime_type)
    crime_table_display = get_crime_type_rate(area_df,city=city,district=lsoa)
    


    if user_add:
        st.write(crime_plot)
        st.write(crime_table_display)
        
