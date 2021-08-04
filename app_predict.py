import pandas as pd
import streamlit as st
from projectUKcrime.user_inputs import user_lat_lon_address
from projectUKcrime.predict import outcome_prediction

def app():
    ## open preidciton module pickle 
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
   
            crime_type = st.sidebar.selectbox("Please choose crime type:",crime_type_list)

            submit_button = st.form_submit_button(label="Submit")

            if submit_button:
                st.sidebar.write("Generating your data")
                
    u_lat, u_lon, u_full_add = user_lat_lon_address(user_add)
    data = [[u_lon, u_lat,crime_type]]
    data_df = pd.DataFrame(data, columns = ['lon', 'lat','crime'])
    pred_proba = model.predict_proba(data_df)
    predict_view = pd.DataFrame(zip(model.classes_,pred_proba[0]))
    predict_view.columns = ['outcome','probability']
    predict_view['probability'] = predict_view['probability'].apply(lambda x: round(x*100,2))
    predict_view = predict_view.sort_values(['probability'], ascending = False)
    predict_view
    if user_add:
        st.write(predict_view)