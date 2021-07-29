import requests
import pandas as pd

# !!! Need to be updated for productions.
raw_data_filepath = '../raw_data/'

#get lists of police regions directly from API
def get_police_regions():
    police_regions = [dic['id'].replace('-',' ') for dic in requests.get("https://data.police.uk/api/forces").json()]
    return police_regions

#get lists of police regions directly from API
def get_crimes():
    crime_list = [dic['name'] for dic in requests.get("https://data.police.uk/api/crime-categories?").json()][1:-1]
    return crime_list

#get lists of monthly files for an area - NOT NEEDED IF USE CLEAN_DATA.
def find_area_files(file_path,area):
    area = area.replace(" ","-")
    files = glob.glob(f'{file_path}/**/*{area}-street.csv',recursive = True)
    return files

#
def create_area_df(area):
    dfs = []
    for file in find_area_files(area): 
        dfs.append(pd.read_csv(file))
    area_df = pd.DataFrame()
    for i in range(len(dfs)): 
        area_df = pd.concat([area_df,dfs[i]]) 
    return area_df

# loads the LSOA DF !!!!!! Need to update the file path at production
def get_lsoa_data():
    lsoapkl_path = raw_data_filepath+'lsoa_data.pkl'
    lsao_df = pd.read_pickle(lsoapkl_path)
    return lsao_df