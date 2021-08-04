import streamlit as st
import pandas as pd
from projectUKcrime.mapping import heat_map

import folium
from streamlit_folium import folium_static

def app():
    st.title('UK crime heatmaps')

    base_map = heat_map(st.session_state.area_df,
                        st.session_state.u_lat,
                        st.session_state.u_lon,
                        user_address=st.session_state.u_full_add,
                        radius = st.session_state.u_radius, 
                        crime_list = st.session_state.crime_type)
    folium_static(base_map,width=800,height=495)