import streamlit as st
import pandas as pd
from datetime import datetime, time
# import pydeck as pdk
import requests

url_example = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?input=1600+Amphitheatre&key=<API_KEY>&sessiontoken=1234567890'
base_url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?input='

pu = False

# title
st.title('UK crime radar')

pu_option = st.sidebar.selectbox(
...     'Select how granular you want your data to be?',
...     ('LSOA', 'City', 'Police Region'))

# pickup
pu = st.sidebar.text_input(label = 'please key in your address in the UK?')

if pu:
    pu = pu +', United Kingdom'
    response = requests.get(f"https://nominatim.openstreetmap.org/search?q={pu}&format=json").json()[0]
    pu_lat = response['lat']
    pu_lon = response['lon']
    pu_full_add = response['display_name']

# map
st.map(pd.DataFrame({'lat': [pu_lat], 'lon': [pu_lon]}))

