import requests

def get_police_regions():
    police_regions = [dic['id'].replace('-',' ') for dic in requests.get("https://data.police.uk/api/forces").json()]
    return police_regions

def get_crimes():
    crime_list = [dic['name'] for dic in requests.get("https://data.police.uk/api/crime-categories?").json()][1:-1]
    return crime_list

def get_neighbourhoods(region):
    regions = get_police_regions()
    if region in regions:
        nbh_list = [dic['name'].replace('-',' ') for dic in requests.get(f"https://data.police.uk/api/{area_list[3]}/neighbourhoods").json()]
        return nbh_list
    else:
        return None


def find_area_files(file_path,area):
    area = area.replace(" ","-")
    files = glob.glob(f'{file_path}/**/*{area}-street.csv',recursive = True)
    return files

def create_area_df(area):
    dfs = []
    for file in find_area_files(area): 
        dfs.append(pd.read_csv(file))
    area_df = pd.DataFrame()
    for i in range(len(dfs)): 
        area_df = pd.concat([area_df,dfs[i]]) 
    return area_df