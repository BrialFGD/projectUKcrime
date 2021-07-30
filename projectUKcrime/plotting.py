import pandas as pd 
import numpy as np
import statistics
import requests
import matplotlib.pyplot as plt
import seaborn as sns

from gata_data import create_area_df

#function that returns crime count by month for a given city & crime type
def get_crime_count(force_df,city = None, crime = None):
    force_df = force_df.dropna(subset = ['LSOA name'], axis = 'rows')
    if city != None:
        force_df['city']=force_df['LSOA name'].apply(lambda x: x[:-5])
        force_df = force_df.loc[force_df['city'] == city]
    if crime != None:
        force_df = force_df.loc[force_df['Crime type'] == crime]
           
    crime_count_df = force_df.groupby(['Month']).agg({'LSOA name':'count'})
    crime_count_df.columns = ['crime_count']
    return crime_count_df

def get_city_population(force, city = None):
    lsoa_df = get_lsoa_data()
    lsoa_df = lsoa_df.loc[lsoa_df['force'] == force]
    if city != None:
        lsoa_df = lsoa_df.loc[lsoa_df['city'] == city]
    return lsoa_df['pop'].sum()

def get_district_population(force, district = None):
    lsoa_df = get_lsoa_data()
    lsoa_df = lsoa_df.loc[lsoa_df['force'] == force]
    if district != None:
        lsoa_df = lsoa_df.loc[lsoa_df['lsoa_name'] == district]
    return lsoa_df['pop'].sum()

def get_crime_rate(force,city = None, crime = None):
    force_df = create_area_df(force)
    crime_count_df = get_crime_count(force_df = force_df,city = city, crime = crime)
    population = get_population(force = force, city = city)
    crime_count_df['crime_rate']=crime_count_df['crime_count'].apply(lambda x: x/population)
    crime_count_df.drop(columns = 'crime_count', inplace = True)
    return crime_count_df

def plot_relative_crime_rate(region,city = None, crime = None):
    force_df = create_area_df(region)
    force_crime_rate = get_crime_rate(region, force_df, crime = crime)
    if city != None:
        city_crime_rate = get_crime_rate(region, force_df,city = city, crime = crime)
        city_crime_rate.columns = ['city_crime_rate']
        city_crime_rate = city_crime_rate.reset_index()
        force_crime_rate = force_crime_rate.reset_index()
        force_crime_rate = force_crime_rate.merge(city_crime_rate, on = 'Month' )
        force_crime_rate = force_crime_rate.set_index('Month')
    plot = force_crime_rate.plot();
    return plot