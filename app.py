import streamlit as st
import app_heat_mapping
import app_time_mapping
import app_plotting
import app_home
import app_predict

from projectUKcrime.gata_data import get_lsoa_data, create_area_df
from projectUKcrime.user_inputs import user_lat_lon_address, get_LSOA_city_region,hs_distance

PAGES = {"Home":app_home,
         "Crime HeatMaps":app_heat_mapping,
         "Crime TimeSeries Map":app_time_mapping,
         "Crime Data":app_plotting,
         "Crime Outcome Prediction":app_predict}
selection = "Home"
st.session_state.selection = selection

st.sidebar.title('UK Crime Tracker')

with st.sidebar:
    with st.form("user inputs"):
        user_add = st.sidebar.text_input(label = 'Please enter an address in the UK?')
        u_radius = st.sidebar.selectbox(
        'Please choose an area size for displaying crime data?',
        ('1', '5', '10','50'))
  
        crime_type_list = ['Anti-social behaviour','Bicycle theft','Burglary','Criminal damage and arson','Drugs','Other theft','Possession of weapons','Public order','Robbery','Shoplifting','Theft from the person','Vehicle crime','Violence and sexual offences']
        crime_type = st.sidebar.multiselect("Please choose crime type:",crime_type_list)

        #move to choose visualization:
        selection = st.sidebar.radio("", list(PAGES.keys()))

        submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            #get all user data in variables
            u_lat, u_lon, u_full_add = user_lat_lon_address(user_add)
            lsoa_df = get_lsoa_data()
            df, lsoa, city, region = get_LSOA_city_region(lsoa_df,u_lon,u_lat)
            area_df = create_area_df(region)
            u_radius = float(u_radius)
        
            #save all user variables to st_session.
            st.session_state.u_lat = u_lat
            st.session_state.u_lon = u_lon
            st.session_state.u_full_add = u_full_add
            st.session_state.area_df = area_df
            st.session_state.lsoa = lsoa
            st.session_state.city = city
            st.session_state.region = region
            st.session_state.u_radius = u_radius
            st.session_state.crime_type = crime_type
            st.session_state.selection = selection  
            
            st.sidebar.write("Please check your full address:")
            st.sidebar.markdown(f"**{st.session_state.u_full_add}**")      

page = PAGES[st.session_state.selection]
page.app()