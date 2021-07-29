import pandas as pd 
import numpy as np
import statistics
import requests
import matplotlib.pyplot as plt
import seaborn as sns

#function that returns crime count by month for a given city & crime type
def get_crime_count(force_df,city = None, crime = None):
    if city != None:
        force_df['city']=force_df['LSOA name'].apply(lambda x: x[:-5])
        force_df = force_df.loc[force_df['city'] == city]
    if crime != None:
        force_df = force_df.loc[force_df['Crime type'] == crime]
           
    crime_count_df = force_df.groupby(['Month']).agg({'LSOA name':'count'})
    crime_count_df.columns = ['crime_count']
    return crime_count_df

def get_population(force, city = None):
    lsoa_df = get_lsoa_data()
    lsoa_df = lsoa_df.loc[lsoa_df['force'] == force]
    if city != None:
        lsoa_df = lsoa_df.loc[lsoa_df['city'] == city]
    
    return lsoa_df['pop'].sum()

def get_crime_rate(force,force_df,city = None, crime = None):
    crime_count_df = get_crime_count(force_df = force_df,city = city, crime = crime)
    population = get_population(force = force, city = city)
    crime_count_df['crime_rate']=crime_count_df['crime_count'].apply(lambda x: x/population)
    return crime_count_df
                