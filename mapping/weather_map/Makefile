get_data: 
	#mkdir intermediary_data_files

	curl -o city_list.txt 'http://openweathermap.org/help/city_list.txt'
	grep 'BR' city_list.txt > city_list_brazil.txt
	head -1  city_list.txt | cat - city_list_brazil.txt > temp && mv temp city_list_brazil.txt
	python3 brazil_fetch_weather.py