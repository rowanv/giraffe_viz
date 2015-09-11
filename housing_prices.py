from bokeh.plotting import figure, output_file, show
from bokeh.embed import components

import pandas as pd
from sklearn.datasets import load_boston
import statsmodels.formula.api as smf

boston = load_boston()
bos = pd.DataFrame(boston.data)
bos.columns = boston.feature_names

bos['price'] = boston.target
bos.head()

lm = smf.ols(formula='price~LSTAT', data=bos)
lm_result = lm.fit()
print(lm_result.summary())

print(lm_result.params)

y_predictions = lm_result.predict()

x = bos.LSTAT
y = bos.price

output_file("housing_prices.html", title="LSTAT vs. Housing Prices Regression")

p = figure(title="Boston Housing Prices vs. LSTAT", x_axis_label="Lower Status of the Population (%) - LSTAT", y_axis_label="Price")

p.scatter(x, y, legend="Actual Values", marker="circle")
p.scatter(x, y_predictions, legend="Predicted Values", color="darkgrey")

#Adding line of best fit from regression model

script_file = open('housing_prices_script.html', 'w+')
div_file = open('housing_prices_div.html', 'w+')

script, div = components(p)
print(script, file=script_file)
print(div, file=div_file)

show(p)

