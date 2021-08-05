import pandas as pd
import streamlit as st
import pickle

def app():
    #Prepare user inputs to prediction model format
    data = [[st.session_state.u_lon,
             st.session_state.u_lat,
             st.session_state.crime_type]]
    X_df = pd.DataFrame(data, columns = ['lon', 'lat','crime'])
    
    #load the fitted preprocessor pickle
    preproc_filepath = 'raw_data/full_fit_preproc.pkl'
    preproc = pickle.load(open(preproc_filepath,'rb'))
    
    #preprocess X_df
    X_preproc_df = preproc.transform(X_df)
    
    #Load the fitted XGBClassifier model
    model_filepath = 'raw_data/big_fit_xgbc.pkl'
    outcome_model = pickle.load(open(model_filepath,'rb'))
    
    #predict and present data
    pred_proba = outcome_model.predict_proba(X_preproc_df)
    predict_view = pd.DataFrame(zip(model.classes_,pred_proba[0]))
    predict_view.columns = ['outcome','probability']
    predict_view['probability'] = predict_view['probability'].apply(lambda x: round(x*100,2))
    predict_view = predict_view.sort_values(['probability'], ascending = False)
    
    st.write(f"Here are the probabities of judicial outcomes for a {st.session_state.crime_type[0]} happending at {st.session_state.u_full_add}")
    
    st.write(predict_view)