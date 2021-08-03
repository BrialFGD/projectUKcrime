import streamlit as st

def app():
    st.markdown("<h1 style='text-align: center; color: white;'>Welcome To The UK Crime Tracker</h1>", unsafe_allow_html=True)
    
    
    st.markdown("""
    -**Crime HeatMaps** lets you see the locational distribution of different crime types in your chosen area.
    
    -**Crime TimeSeries Map** lets you see the locational distribution of different crime types in your chosen area over time.
    
    -**Crime Data** lets you compare trends in crime data in your local area and region.
    
    
    -The UK Crime Tracker was created by Brial, Blair and Andrew at Le Wagon Shaghai.
    """)
    
    