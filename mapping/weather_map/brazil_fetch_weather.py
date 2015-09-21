import json
import urllib.request
import pandas as pd

city_ids = [ 3663517, 3462916, 3664980]
city_ids = [str(x) for x in city_ids]
joined_city_ids = ','.join(city_ids)


url = 'http://api.openweathermap.org/data/2.5/box/city?bbox=-34,5,-73,-33,6&cluster=yes&country=BR&units=metric'

url_old = 'http://api.openweathermap.org/data/2.5/group?id=%s&units=metric' % joined_city_ids



OUTFILE = 'cleaned_brazil_weather_data.json'

response = urllib.request.urlopen(url) 
str_response = response.readall().decode('utf-8')
data = json.loads(str_response) 

with open('intermediary_test', 'w') as outfile:
	json.dump(data, outfile)



weather_df = pd.DataFrame.from_dict([x for x in data['list']])
cities_df = pd.DataFrame.from_csv('city_list_brazil.txt', sep='\t')

joined_weather_dfs = weather_df.merge(cities_df, how='inner', left_on='name', right_on='nm')
joined_weather_dfs.fillna('NULL', inplace=True)

joined_weather_dict = joined_weather_dfs.to_dict(orient='records')


data['list'] = joined_weather_dict

with open(OUTFILE, 'w') as outfile:
    json.dump(data, outfile)