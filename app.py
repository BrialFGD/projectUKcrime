import streamlit as st
import app_heat_mapping
import app_time_mapping
import app_plotting
import app_home

PAGES = {"Home":app_home,
         "Crime HeatMaps":app_heat_mapping,
         "Crime TimeSeries Map":app_time_mapping,
         "Crime Data":app_plotting
    
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()