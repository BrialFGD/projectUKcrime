import streamlit as st
import pandas as pd
from streamlit.proto.RootContainer_pb2 import SIDEBAR
from projectUKcrime.gata_data import get_lsoa_data, create_area_df
from projectUKcrime.user_inputs import user_lat_lon_address, get_LSOA_city_region,hs_distance
from projectUKcrime.mapping import heat_map_time
import folium
from streamlit_folium import folium_static

def app():
    st.title(f'UK {st.session_state.crime_type[0]} crimes heatmaps over last 36 months')

    base_map = heat_map_time(st.session_state.area_df,st.session_state.u_lat,st.session_state.u_lon,user_address=st.session_state.u_full_add,radius = st.session_state.u_radius, crime= st.session_state.crime_type[0])

    folium_static(base_map,width=800,height=700)