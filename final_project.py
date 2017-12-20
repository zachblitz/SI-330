import requests
import csv
import json
from pprint import pprint


def get_rating_avg(x):
	total = sum(x)
	return round((total/len(x)), 1)

countries = []
country_rating_dict = {}
average_rating_by_country = {}
country_population_dict = {}
with open('fifa_dataset.csv', 'r', newline = '', encoding='iso-8859-1') as input_file:
	fifa_reader = csv.DictReader(input_file, delimiter = ',') #, quotechar = '"')
	
	for row in fifa_reader:
		if row['Nationality'] == 'Wales':
			continue
		if row['Nationality'] == 'England':
			continue
		if row['Nationality'] == 'Cape Verde':
			continue
		if row['Nationality'] == 'Scotland':
			continue
		if row['Nationality'] == 'Kosovo':
			continue
		if row['Nationality'] == 'Guinea Bissau':
			continue
		if row['Nationality'] == 'St Kitts Nevis':
			continue
		if row['Nationality'] == 'St Lucia':
			continue
		if row['Nationality'] == 'Czech Republic':
			continue
		if row['Nationality'] == 'Northern Ireland':
			continue
		if row['Nationality'] == 'Bosnia Herzegovina':
			row['Nationality'] = 'Bosnia and Herzegovina'
		if row['Nationality'] == 'Ivory Coast':
			row['Nationality'] = "Côte d'Ivoire"
		if row['Nationality'] == 'Guinea':
			row['Nationality'] = "Papua New Guinea"
		if row['Nationality'] == 'Korea Republic':
			row['Nationality'] = "Korea (Republic of)"
		if row['Nationality'] == 'DR Congo':
			row['Nationality'] = "Congo (Democratic Republic of the)"
		if row['Nationality'] == 'Russia':
			row['Nationality'] = "Russian Federation"
		if row['Nationality'] == 'Republic of Ireland':
			row['Nationality'] = "Ireland"
		if row['Nationality'] == 'United States':
			row['Nationality'] = "United States of America"
		if row['Nationality'] == 'Venezuela':
			row['Nationality'] = "Venezuela (Bolivarian Republic of)"
		if row['Nationality'] == 'Syria':
			row['Nationality'] = "Syrian Arab Republic"
		if row['Nationality'] == 'Iran':
			row['Nationality'] = "Iran (Islamic Republic of)"
		if row['Nationality'] == 'China PR':
			row['Nationality'] = "China"
		if row['Nationality'] == 'Moldova':
			row['Nationality'] = "Moldova (Republic of)"
		if row['Nationality'] == 'Bolivia':
			row['Nationality'] = "Bolivia (Plurinational State of)"
		if row['Nationality'] == 'FYR Macedonia':
			row['Nationality'] = "Macedonia (the former Yugoslav Republic of)"
		if row['Nationality'] == 'Curacao':
			row['Nationality'] = "Curaçao"
		if row['Nationality'] == 'Trinidad & Tobago':
			row['Nationality'] = "Trinidad and Tobago"
		if row['Nationality'] == 'Tanzania':
			row['Nationality'] = "Tanzania, United Republic of"
		if row['Nationality'] == 'Korea DPR':
			row['Nationality'] = "Korea (Democratic People's Republic of)"
		if row['Nationality'] == 'Palestine':
			row['Nationality'] = "Palestine, State of"
		if row['Nationality'] == 'Central African Rep.':
			row['Nationality'] = "Central African Republic"
		if row['Nationality'] == 'Antigua & Barbuda':
			row['Nationality'] = "Antigua and Barbuda"
		if row['Nationality'] == 'Vietnam':
			row['Nationality'] = "Viet Nam"

		country = row['Nationality']
		if country not in countries:
			countries.append(country)
		else:
			pass
		rating = int(row['Overall'])
		values = []
		values.append(rating)
		if country not in country_rating_dict:
			country_rating_dict[country] = values
		else:
			country_rating_dict[country].append(rating)


	for country in country_rating_dict:
		average = get_rating_avg(country_rating_dict[country])
		average_rating_by_country[country] = average

cache_data = 'fifa.json'

try:
	rest_cache_file = open(cache_data, 'r')
	rest_cache_contents = rest_cache_file.read()
	my_cache_diction = json.loads(rest_cache_contents)
	rest_cache_file.close()

except:
	my_cache_diction = {}


for x in countries:
	if x in my_cache_diction:
		population = my_cache_diction[x][0]['population']
		country_population_dict[x] = population
		
	else:
		url = "https://restcountries.eu/rest/v2/name/" + x + "?fullText=true"
		r = requests.get(url)
		responses = r.text
		done = json.loads(responses)
		my_cache_diction[x] = done
		rest_cache_file = open(cache_data, 'w')
		rest_cache_file.write(json.dumps(my_cache_diction))
		rest_cache_file.close()
		population = done[0]['population']
		country_population_dict[x] = population


with open('fifa_final_output.csv', 'w', newline = '', encoding='iso-8859-1') as output_file:
	fifa_writer = csv.DictWriter(output_file, fieldnames = ['Country', 'Average FIFA Rating', 'Population'], delimiter = ',', quotechar = '"')
	fifa_writer.writeheader()

	data = {}

	for country in countries:
		data['Country'] = country
		data['Average FIFA Rating'] = average_rating_by_country[country]
		data['Population'] = country_population_dict[country]
		fifa_writer.writerow(data)


#now to find correlation
mean_rating = round(sum(average_rating_by_country.values()) / len (average_rating_by_country.values()),1)
mean_population = round(sum(country_population_dict.values()) / len (country_rating_dict.values()),1)

total_rating = 0
total_population = 0

rat = 0
pop = 0

for country in countries:
	rating_difference_squared = round((float(average_rating_by_country[country]) - float(mean_rating)),1)**2
	total_rating += rating_difference_squared

	num = float(average_rating_by_country[country]) - float(mean_rating)
	rat += num
	

	pop_difference_squared = round((float(country_population_dict[country]) - float(mean_population)),1)**2
	total_population += pop_difference_squared

	toe = float(country_population_dict[country]) - float(mean_population)
	pop += toe
	

inside_x = (total_rating / len(countries) - 1)
inside_y = (total_population / len(countries) - 1)

std_x = inside_x**(1/2)
std_y = inside_y**(1/2)


denom = std_x * std_y

num = pop*rat

r = (len(countries) -1) * ((num / denom))
print(r)


	