from hashlib import new
import json
from bs4 import BeautifulSoup
from dateutil import parser
import requests, cloudscraper
import collections
scraper = cloudscraper.create_scraper()

req = scraper.get('https://www.un.org/fr/observances/list-days-weeks')
bs = BeautifulSoup(req.content, "html.parser")

rows = bs.find_all('div', {'class': 'views-row'})

data = {}
for row in rows:
    date = parser.parse(row.find('span', {'class': 'date-display-single'})['content'])
    date = date.replace(year=2022)
    title = row.find('span', {'class': 'views-field-title'}).text
    data[date] = title

from pprint import pprint
new_data = {}
ord = collections.OrderedDict(sorted(data.items()))
for key, value in dict(ord).items():
    new_data[key.strftime('%d/%m')]= value

with open('international_day.json', 'w', encoding='utf8') as file:
    json.dump(new_data, file, ensure_ascii=False, indent=4)

