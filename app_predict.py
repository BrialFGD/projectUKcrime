import pandas as pd
import streamlit as st
import pickle
import sklearn

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
    model_filepath = open('raw_data/big_fit_log.pkl','rb')
    outcome_model = pickle.load(model_filepath)
    model_filepath.close()
    
    #predict and present data
    pred_proba = outcome_model.predict_proba(X_preproc_df)
    predict_view = pd.DataFrame(zip(outcome_model.classes_,pred_proba[0]))
    predict_view.columns = ['outcome','probability']
    predict_view['probability'] = predict_view['probability'].apply(lambda x: round(x*100,2))
    predict_view = predict_view.sort_values(['probability'], ascending = False)
    
    outcome_dict = {'investigation completed, pending court action':'Court case in progress',
                    'court_ruled':'Court judgement issued',
                    'case proceedings not in the public interest':'Prosecution not in the public interest',
                    'no investigation':'No investigation',
                    'case found non-judicial resolution':'Case resolved outside of the courts',
                    'investigation completed, no court proceeding':'No court action',
                    'Under investigation':'Case still under investigation'}

    predict_view['outcome'] = predict_view['outcome'].map(outcome_dict)
    predict_view = predict_view.set_index('outcome')
    
    st.title(f"Here are the probabities of judicial outcomes for a {st.session_state.crime_type[0]} crime located at {st.session_state.u_full_add}")
    
    st.write(predict_view)