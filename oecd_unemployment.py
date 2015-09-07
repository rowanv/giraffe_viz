from collections import OrderedDict

from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource, Range1d

import pandas as pd



df = pd.read_csv('~/Google Drive/Datasets/OECD_Labour_Stats.csv')


years = Range1d(1995, 2015)
countries = list(set(df['Country'].values))

colours = [
    "#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce",
    "#ddb7b1", "#cc7878", "#933b41", "#550b1d"
]

df['colours'] = [colours[min(int(rate) - 2, 8)] for rate in df['Value'].values]

source = ColumnDataSource(df)

output_file('oecd_unemployment.html')

p = figure(title='OECD Unemployment (1990 - 2015)',
          tools='resize,hover,save', x_range=years, y_range=countries)
p.rect(x='Time', y='Country', width=1, height=1, source=source,
       color='colours', line_color=None)


hover = p.select(dict(type=HoverTool))
hover.tooltips = OrderedDict([
        ('Year', '@Time'),
        ('Country', '@Country'),
        ('Unemployment Rate (%)', '@Value')
    ])
p.toolbar_location = 'right'
p.plot_height = 800
p.plot_width = 1000

#Getting rid of chart junk
p.outline_line_color = None
p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.minor_tick_line_color = None

show(p)