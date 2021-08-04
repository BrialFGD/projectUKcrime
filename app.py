import streamlit as st
import app_heat_mapping
import app_time_mapping
import app_plotting
import app_home
import app_predict

PAGES = {"Home":app_home,
         "Crime HeatMaps":app_heat_mapping,
         "Crime TimeSeries Map":app_time_mapping,
         "Crime Data":app_plotting,
         "Crime Outcome Prediction":app_predict
    
}
st.sidebar.title('UK Crime Tracker')
selection = st.sidebar.radio("", list(PAGES.keys()))
page = PAGES[selection]
page.app()