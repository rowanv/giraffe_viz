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