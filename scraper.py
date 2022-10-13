import json
from bs4 import BeautifulSoup
from dateutil import parser
import cloudscraper
import collections

def get_data(rows, ):
    data = {}
    new_data = {}
    for row in rows:
        date = parser.parse(row.find('span', {'class': 'date-display-single'})['content'])
        date = date.replace(year=2022)
        if date not in data.keys():
            data[date] = []

        title = row.find('span', {'class': 'views-field-title'}).text
        
        data[date].append(title)
    ord = collections.OrderedDict(sorted(data.items()))
    for key, value in dict(ord).items():
        new_data[key.strftime('%d/%m')]= value
    return new_data

scraper = cloudscraper.create_scraper()

req_en = scraper.get('https://www.un.org/en/observances/list-days-weeks')
req_fr = scraper.get('https://www.un.org/fr/observances/list-days-weeks')

bs_en = BeautifulSoup(req_en.content, "html.parser")
bs_fr = BeautifulSoup(req_fr.content, "html.parser")

rows_fr = bs_fr.find_all('div', {'class': 'views-row'})
rows_en = bs_en.find_all('div', {'class': 'views-row'})


data = {
    'en':get_data(rows_en), 
    'fr': get_data(rows_fr)
}


with open('international_day.json', 'w', encoding='utf8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
