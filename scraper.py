from hashlib import new
import json
from bs4 import BeautifulSoup
from dateutil import parser
import cloudscraper
import collections
scraper = cloudscraper.create_scraper()

req_en = scraper.get('https://www.un.org/en/observances/list-days-weeks')
req_fr = scraper.get('https://www.un.org/fr/observances/list-days-weeks')

bs_en = BeautifulSoup(req_en.content, "html.parser")
bs_fr = BeautifulSoup(req_fr.content, "html.parser")

rows_fr = bs_fr.find_all('div', {'class': 'views-row'})
rows_en = bs_en.find_all('div', {'class': 'views-row'})


data = {}
i = 0
while i < len(rows_fr):
    date = parser.parse(rows_fr[i].find('span', {'class': 'date-display-single'})['content'])
    date = date.replace(year=2022)
    title_fr = list(rows_fr)[i].find('span', {'class': 'views-field-title'}).text
    title_en = list(rows_en)[i].find('span', {'class': 'views-field-title'}).text

    data[date] = {'en': title_en, 'fr':title_fr}
    i+=1

new_data = {}
ord = collections.OrderedDict(sorted(data.items()))
for key, value in dict(ord).items():
    new_data[key.strftime('%d/%m')]= value

with open('international_day.json', 'w', encoding='utf8') as file:
    json.dump(new_data, file, ensure_ascii=False, indent=4)

