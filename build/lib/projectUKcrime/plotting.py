import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from projectUKcrime.gata_data import get_lsoa_data

#function that returns crime count by month for a given city & crime type
def get_crime_count(area_df,city = None, crime = None):
    force_df = area_df
    force_df = force_df.dropna(subset = ['LSOA name','Crime type'], axis = 'rows')
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

def get_city_crime_rate(area_df,city = None, crime = None):
    force_df = area_df
    force = list(force_df['Falls within'])[0]
    crime_count_df = get_crime_count(area_df = force_df,city = city, crime = crime)
    population = get_city_population(force = force, city = city)
    crime_count_df['crime_rate']=crime_count_df['crime_count'].apply(lambda x: (x/population)*1000*12)
    crime_count_df.drop(columns = 'crime_count', inplace = True)
    return crime_count_df

def plot_relative_crime_rate(area_df,city = None, crime = None):
    force_df = area_df
    
    force_df['city']=force_df['LSOA name'].apply(lambda x: x[:-5])
    force_crime_rate = get_city_crime_rate(force_df, crime = crime)
    if city != None:
        city_crime_rate = get_city_crime_rate(force_df,city = city, crime = crime)
        city_crime_rate.columns = ['city_crime_rate']
        city_crime_rate = city_crime_rate.reset_index()
        force_crime_rate = force_crime_rate.reset_index()
        force_crime_rate = force_crime_rate.merge(city_crime_rate, on = 'Month' )
        #force_crime_rate = force_crime_rate.set_index('Month')
    
    sns.set_style("dark")
    fig = plt.figure(figsize=(25,20))
    ax = sns.lineplot(data=force_crime_rate[['city_crime_rate','Month']],x="Month",y="city_crime_rate",palette=['red'], linewidth=2.5)
    ax = sns.lineplot(data=force_crime_rate[['crime_rate','Month']],x="Month",y="crime_rate",palette=['blue'], linewidth=2.5)
    ax.set_xticks(ax.get_xticks()[::3])
    plt.xticks(fontsize=20,rotation=45)
    plt.yticks(fontsize=20)
    plt.xlabel("")
    plt.ylabel("")
    
    return fig

def get_crime_type_rate(area_df, city = None, district = None):
    #pull database for the force
    force_df = area_df
    region = list(force_df['Falls within'])[0]
    
    #clean NA if any
    force_df = force_df.dropna(subset = ['LSOA name','Crime type'],axis = 0)
    
    
    #Create city columns
    force_df['city']=force_df['LSOA name'].apply(lambda x: x[:-5])
    
    #create region count by crime types.
    region_crimes = force_df.groupby(['Crime type']).agg({'LSOA name':'count'})
    region_crimes = region_crimes.reset_index()
    region_crimes["category"] = region
    region_crimes.columns = ['Crime types', 'count','category']
    
    #create city count by crime types.
    city_crimes = force_df[force_df['city'] == city].groupby(['Crime type']).agg({'LSOA name':'count'})
    city_crimes = city_crimes.reset_index()
    city_crimes["category"]=city
    city_crimes.columns = ['Crime types', 'count','category']
    
    #create district count by crime types.
    #district_crimes = force_df[force_df['LSOA name'] == district].groupby(['Crime type']).agg({'LSOA name':'count'})
    #district_crimes = district_crimes.reset_index()
    #district_crimes.columns = ['Crime types', 'district_count']
    
    #Merge Region-City-District data on crime types
    #region_crimes = region_crimes.merge(city_crimes, on = 'Crime types').merge(district_crimes, on = 'Crime types')
    
    #get populations:
    region_pop = get_city_population(region)
    city_pop = get_city_population(region, city)
    district_pop = get_district_population(region, district)
    
    #Normalize Region-City-District to population:
    region_crimes['rate']=region_crimes['count'].apply(lambda x: round((x/region_pop*1000)/3,2))
    city_crimes['rate']=city_crimes['count'].apply(lambda x: round((x/city_pop*1000)/3,2))
    #region_crimes['district_rate']=region_crimes['district_count'].apply(lambda x: round((x/district_pop*1000)/3,2))
    
    #drop count columns to keep rates:
    #region_crimes = region_crimes.drop(columns = ['region_count','city_count','district_count'])
    #region_crimes = region_crimes.set_index('Crime types')
    #region_crimes = region_crimes.sort_values('region_rate', ascending=False)
    # dropping LSOA for simplicity 
    #region_crimes = region_crimes.drop(columns='district_rate')
    region_crimes = pd.concat([city_crimes,region_crimes])
    region_crimes = region_crimes.drop(columns="count")
    return region_crimes

def plot_relative_crime_rate_bar(area_df, city = None, district = None):
    region_df = get_crime_type_rate(area_df, city, district)
    sns.set_style("dark")
    fig = plt.figure(figsize=(25,20))
    ax = sns.barplot(data=region_df,y="Crime types",x="rate",hue="category")
    plt.legend(loc='best',fontsize=25)
    plt.setp(ax.get_legend().get_texts(), fontsize='25')
    plt.setp(ax.get_legend().get_title(), fontsize='0')
   
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.xlabel("")
    plt.ylabel("")
    return fig
    