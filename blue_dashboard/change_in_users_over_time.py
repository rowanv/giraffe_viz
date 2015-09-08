from collections import OrderedDict

import tweepy
import requests
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource, Range1d

from config import auth, twittercounter_com_key



user = 'Android'
android_user_id = 382267114



api = tweepy.API(auth)

twittercount_url = 'http://api.twittercounter.com?twitter_id='+ str(android_user_id) + '&apikey=' + twittercounter_com_key
r = requests.get(twittercount_url)


user_follower_nums_dict = r.json()['followersperdate']
user_follower_df = pd.DataFrame.from_dict(user_follower_nums_dict, orient='index')
user_follower_df.columns = ['number of users']


cleaned_date_strings = [date_string[9:] for date_string in user_follower_df.index]

user_follower_df = user_follower_df.set_index([cleaned_date_strings])

change_in_users = []
change_in_users.append(0)
for n, elem in enumerate(user_follower_df['number of users'].values[1:]):
    #subtract from the previous week's value
    change_in_users.append(user_follower_df['number of users'][n] - elem)
change_in_users

user_follower_df['change in users'] = change_in_users



source = ColumnDataSource(user_follower_df)
output_file('blue_dashboard.html')

dates = list(user_follower_df.index)
users_range = Range1d(0, 9000000)
users_change_range = Range1d(min(user_follower_df['change in users'].values),
	max(user_follower_df['change in users'].values) + 100)

p = figure(title='Day to Day Change In Twitter Users', tools='resize,hover,save',
	x_range=dates, y_range=users_change_range)
p.line(x='index', y='change in users', source=source)
p.plot_width = 1000
p.plot_height = 500
p.outline_line_color = None
hover = p.select(dict(type=HoverTool))
hover.tooltips = OrderedDict([
        #('Change in Users', '@change in users'),
        ('Day', '@index')
    ])
p.grid.grid_line_color = None
p.ygrid.band_fill_alpha = 0.05
p.ygrid.band_fill_color = 'navy'

show(p)