import json
import pandas as pd



OUTFILE = 'joined_brazil_weather_data.json'

with open('cleaned_brazil_weather_data.json') as data_file:
    data_1 = json.load(data_file)

with open('cleaned_brazil_weather_1442934558.json') as data_file:
    data_2 = json.load(data_file)

weather_df_1 = pd.DataFrame.from_dict([x for x in data_1['list']])
print(weather_df_1['time_collected'][0])

weather_df_2 = pd.DataFrame.from_dict([x for x in data_2['list']])
print(weather_df_2['time_collected'][0])

weather_df_1 = weather_df_1.append(weather_df_2)
weather_df_1.fillna('NULL', inplace=True)

joined_weather_dict = weather_df_1.to_dict(orient='records')


data_1['list'] = joined_weather_dict

with open(OUTFILE, 'w') as outfile:
    json.dump(data_1, outfile)