import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
from time import sleep

ua = UserAgent()

headers = {
    'accept': 'application/json, text/plain, */*',
    'user-Agent': ua.google,
}

gte = int(input('Set the under price: '))
lte = int(input('set the top price: '))

cars_list = []

for p in range(0, 8):

    url = f'https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&year[0].gte=2003&categories.main.id=1&brand.id[0]=52&country.import.usa.not=-1&price.USD.gte={gte}&price.USD.lte={lte}&price.currency=1&gearbox.id[0]=1&fuel.id[3]=4&sort[0].order=dates.created.desc&abroad.not=0&custom.not=1&page={p}&size=20'

    r = requests.get(url)
    sleep(3)

    soup = BeautifulSoup(r.text, 'lxml')

    cars = soup.findAll('div', class_='content-bar')

    for car in cars:
        if car.find('a', class_='banner-link'):  # Skip the add position
            continue
        link = car.find('div', class_='item ticket-title').find('a').get('href')
        title = car.find('div', class_='item ticket-title').find('a').get('title')
        generation = car.find('div', class_='generation').text
        price = car.find('div', class_='price-ticket').text
        race = car.find('li', class_='item-char js-race').text
        location = car.find('li', class_='item-char view-location js-location').text
        fuel = car.findAll('li', class_='item-char')[2].text
        transmission = car.findAll('li', class_='item-char')[3].text
        try:
            description = car.find('div', class_='definition-data').find('p',
                                                                         class_='descriptions-ticket').find(
                'span').text
        except:
            description = ' - '

        cars_list.append([link, title, generation, price, race, location, fuel, transmission, description])

header = ['link', 'title', 'generation', 'price', 'race', 'location', 'fuel', 'transmission', 'description']

print(len(cars_list))  # find how many cars in a search

df = pd.DataFrame(cars_list, columns=header)
df.to_excel('\Lancer_list.xlsx')
