import requests
import haversine as hs

# returns the user latitude, longitude, address from string input on UI
def user_lat_lon_address(input_string):
    pu = input_string+", united kingdom"
    response = requests.get(f"https://nominatim.openstreetmap.org/search?q={pu}&format=json").json()[0]
    pu_lat = float(response['lat'])
    pu_lon = float(response['lon'])
    pu_full_add = response['display_name']
    return pu_lat, pu_lon, pu_full_add

def hs_distance(lat1, long1, lat2, long2):
    loc1 = (lat1, long1)
    loc2 = (lat2, long2)
    return hs.haversine(loc1,loc2)

def get_LSOA_city_region(df,long,lat):
    df['distance'] = df[['Longitude','Latitude']].apply(lambda x: hs_distance(x[1], x[0], lat2=lat, long2=long),axis=1)
    indx = df[['distance']].idxmin()[0]    
    lsoa = df.iloc[indx]['LSOA name']
    city = lsoa[:-5]
    region = df.iloc[indx]['Reported by']
    return df, lsoa, city, region

