import requests
import pandas as pd

# !!! Need to be updated for productions.
raw_data_filepath = 'raw_data/'

#get lists of monthly files for an area - NOT NEEDED IF USE CLEAN_DATA.
def find_area_files(file_path,area):
    area = area.replace(" ","-")
    files = glob.glob(f'{file_path}/**/*{area}-street.csv',recursive = True)
    return files

#
def create_area_df(area):
    area_path = f"{raw_data_filepath}{area}.pkl"
    area_df = pd.read_pickle(area_path)
    return area_df

# loads the LSOA DF !!!!!! Need to update the file path at production
def get_lsoa_data():
    lsoapkl_path = raw_data_filepath+'lsoa_data.pkl'
    lsao_df = pd.read_pickle(lsoapkl_path)
    return lsao_df