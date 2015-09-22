set -e
set -x

now=`date +"%s"`
file_name="cleaned_brazil_weather_$now.json"
cd /Users/rowan/workspace/giraffe_viz/mapping/weather_map/
mv cleaned_brazil_weather_data.json $file_name

 /Users/rowan/virtualenvs/r/bin/python3venv/bin/python3 /Users/rowan/workspace/giraffe_viz/mapping/weather_map/brazil_fetch_weather.py