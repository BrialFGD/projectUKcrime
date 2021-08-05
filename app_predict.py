import pandas as pd
import streamlit as st
import pickle
import xgboost as xgb

def app():
    #Prepare user inputs to prediction model format
    data = [[st.session_state.u_lon,
             st.session_state.u_lat,
             st.session_state.crime_type[0]]]
    X_df = pd.DataFrame(data, columns = ['lon', 'lat','crime'])
    
    #load the fitted preprocessor pickle
    preproc_filepath = 'raw_data/full_fit_preproc.pkl'
    preproc = pickle.load(open(preproc_filepath,'rb'))
    
    #preprocess X_df
    X_preproc_df = preproc.transform(X_df)
    
    #Load the fitted XGBClassifier model - JSON
    #model_filepath = 'raw_data/mini_fit_xgbc.json'
    #outcome_model = xgb.Booster()
    #outcome_model.load_model(model_filepath)
    
    #Load the fitted XGBClassifier model - PKL
    model_filepath = open('raw_data/mini_fit_xgbc.pkl','rb')
    outcome_model = pickle.load(model_filepath)
    model_filepath.close()
    
    #predict and present data
    pred_proba = outcome_model.predict_proba(X_preproc_df)
    predict_view = pd.DataFrame(zip(outcome_model.classes_,pred_proba[0]))
    predict_view.columns = ['outcome','probability']
    predict_view['probability'] = predict_view['probability'].apply(lambda x: round(x*100,2))
    predict_view = predict_view.sort_values(['probability'], ascending = False)
    
    st.write(f"Here are the probabities of judicial outcomes for a {st.session_state.crime_type[0]} crime located at {st.session_state.u_full_add}")
    
    st.write(predict_view)