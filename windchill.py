from math import sqrt
from collections import OrderedDict

from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource, Range1d
import pandas as pd
import numpy as np



def calculate_windchill_temperature(amb_temp, windspeed):
	"""Uses Siple's formula to calculate windchill temperature
	amb_temp: ambient temperature in celsius
	windspeed: windspeed in m/s
	returns: twc - windchill temperature in celsius"""
	twc = 33 + (amb_temp - 33) * (.474 + .454 * sqrt(windspeed) - 0.0454 * windspeed )
	return(twc)

def windchill_to_discrete(twc):
	if twc > 0 :
		return 'Greater than 0'
	elif twc > -10:
		return '-10 to 0'
	elif twc > -20:
		return '-20 to -10'
	elif twc > -30:
		return '-30 to -20'
	elif twc > -40:
		return '-40 to -30'
	elif twc > -50:
		return '-50 to -40'
	elif twc > -60:
		return '-60 to -50'
	else:
		return 'NaN'

colourmap = {
	'Greater than 0': '#ffffd9',
	'-10 to 0': '#edf8b1',
	'-20 to -10': '#c7e9b4',
	'-30 to -20': '#7fcdbb',
	'-40 to -30': '#41b6c4',
	'-50 to -40': '#1d91c0',
	'-60 to -50': '#2225ea8',
	'NaN': '#0c2c84',
}

#Creating windchill dataframe

windspeed = list(range(2, 28, 2))
amb_temp = list(range(8, -32, -2))

windchill_values = [calculate_windchill_temperature(at, w) for w in windspeed for at in amb_temp]
windchill_values = [round(w, 0) for w in windchill_values]
windspeed_values = [at for w in windspeed for at in amb_temp]
amb_temp_values = [w for w in windspeed for at in amb_temp]





windchill_df = pd.DataFrame(data=windchill_values, columns=['windchill'])
discrete_values = [windchill_to_discrete(x) for x in windchill_df['windchill']]
colourmap_values = [colourmap[d] for d in discrete_values]

windchill_df['windspeed'] = windspeed_values
windchill_df['amb_temp'] = amb_temp_values
windchill_df['discrete'] = discrete_values
windchill_df['colourmap'] = colourmap_values



windspeed_range_set = OrderedDict.fromkeys([c for c in windchill_df['windspeed']])
windspeed_range = []
for w in windspeed_range_set:
    windspeed_range.append(str(w))
windspeed_range = windspeed_range


amb_temp_range = set([(i) for i in windchill_df['amb_temp']])
amb_temp_range = [str(a) for a in amb_temp_range]



#Converting the DF to Bokeh's Column Data Source
source = ColumnDataSource(windchill_df)


#Drawing the Bokeh plot

output_file('windchill_table.html')

p = figure(title='Windchill', tools='resize,hover,save', x_axis_label='Windspeed',
           y_axis_label='Ambient Temperature')
p.toolbar_location = 'right'
p.circle('windspeed', 'amb_temp', width=1.2, height=1.2,
         radius=0.5, source=source, fill_alpha=0.6, color='colourmap')
p.x_range = Range1d(-32, 10)
p.y_range = Range1d(0, 27)
hover = p.select(dict(type=HoverTool))
hover.tooltips = OrderedDict([
        ('windchill', '@windchill')
    ])

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.outline_line_color = None
p.xaxis.minor_tick_line_color = None
p.yaxis.minor_tick_line_color = None
p.xaxis.axis_label_text_font_size = '1em'
p.yaxis.axis_label_text_font_size = '1em'
p.title_text_font = 'palatino'
p.xaxis.axis_label_text_font = 'palatino'
p.yaxis.axis_label_text_font = 'palatino'
show(p)

