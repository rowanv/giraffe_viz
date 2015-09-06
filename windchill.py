from math import sqrt
from collections import OrderedDict

from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource
import pandas as pd
import numpy as np



def calculate_windchill_temperature(amb_temp, windspeed):
	"""Uses Siple's formula to calculate windchill temperature
	amb_temp: ambient temperature in celsius
	windspeed: windspeed in m/s
	returns: twc - windchill temperature in celsius"""
	twc = 33 + (amb_temp - 33) * (.474 + .454 * sqrt(windspeed) - 0.0454 * windspeed )
	return(twc)

#Creating windchill table

windspeed = list(range(2, 28, 2))
amb_temp = list(range(8, -32, -2))

windchill_values = [calculate_windchill_temperature(at, w) for w in windspeed for at in amb_temp]
windchill_values = [round(w, 1) for w in windchill_values]
windchill_array = np.array(windchill_values )
windchill_array = np.reshape(windchill_array, (20, 13))

windchill_df = pd.DataFrame(data=windchill_array, index=amb_temp, columns=windspeed)

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

windchill_discrete = map(lambda x: windchill_to_discrete(twc), windchill_df.values

windspeed_range = [str(c) for c in windchill_df.columns]
amb_temp_range = [str(i) for i in windchill_df.index]


colormap = {
	'Greater than 0': '#ffffcc',
	'-10 to 0': '#a1dab4',
	'-20 to -10': '#41b6c4',
	'-30 to -20': '#225ea8',
	'-40 to -30': '#bdbdbd',
	'-50 to -40': '#bdbdbd',
	'-60 to -50': '#bdbdbd',
	'NaN': '#bdbdbd',
}

source = ColumnDataSource(
	data = dict(
		twc=windchill_df.values
		windspeed = windchill_df.columns
		amb_temp = windchill_df.index
		discrete= [windchill_to_discrete(twc) for twc in windchill_df.values]))

output_file('windchill_table.html')

p = figure(title='Windchill', tools='resize,hover,save', x_range=windspeed_range, y_range=amb_temp_range)
p.plot_width = 1200
p.toolbar_location = 'left'
p.rec('group', 'period', 0.9, 0.9, source=source, fill_alpha=0.6, color='type_color')
show(p)

#Maybe change the format of the data frame


