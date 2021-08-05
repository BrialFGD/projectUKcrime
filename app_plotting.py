import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from projectUKcrime.plotting import plot_relative_crime_rate,get_crime_type_rate,plot_relative_crime_rate_bar

def app():
    st.markdown('**All crime rates are given as crime incidences per 1000 residents per month**')
    
    crime_plot = plot_relative_crime_rate(st.session_state.area_df,st.session_state.city,st.session_state.crime_type[0])
    plt.legend([f"{st.session_state.crime_type[0]} in {st.session_state.city}",f"{st.session_state.crime_type[0]} in {st.session_state.region} Area",],fontsize=25)
    
    crime_table_plot = plot_relative_crime_rate_bar(st.session_state.area_df,city=st.session_state.city, district=st.session_state.lsoa)
     
    if st.session_state.u_full_add:
        st.pyplot(crime_plot)
        st.pyplot(crime_table_plot)