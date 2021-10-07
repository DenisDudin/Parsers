import csv
import re

import requests
from bs4 import BeautifulSoup


class Cards(object):
    base_url = 'https://snol-term.ru'
    cardLinks = []
    def __init__(self):
        pass


def get_html(url):
    r = requests.get(url)
    return r.text


def get_group(html):
    soup = BeautifulSoup(html, 'lxml')
    listGroup = []
    for group in soup.find_all('a', class_='aside__link'):
        listGroup.append(group.get('href'))

    return listGroup


def get_link_cards(html):
    soup = BeautifulSoup(html, 'lxml')
    for card in soup.find_all('a', class_='catalog__item'):
        Cards.cardLinks.append(Cards.base_url+card.get('href'))

    return Cards.cardLinks

def get_information_card():
    # for i in range(len(Cards.cardLinks)):
    for i in range(3):
        r = get_html(Cards.cardLinks[i])
        soup = BeautifulSoup(r, 'lxml')
        card = soup.find('div', class_='card')

        try:
            title = soup.find('h1', class_='head__page-title').text.strip()
        except:
            title = ''
        try:
            photo = Cards.base_url + card.find('img').get('src')
        except:
            photo = ''
        try:
            price = re.findall(r'\d*\.\d+|\d+', card.find('span', class_='card__order-price').text.strip())[0]
        except:
            price = ''
        try:
            currency = card.find('span', class_='card__order-price').text.strip()[-1]
        except:
            currency = ''
        try:
            description = card.find('li', class_='tab-content__item')
        except:
            description = ''
        try:
            characterTitle = []
            characterTitles = card.find('div', class_='card__tabs tabs').find_all('span', class_='character__label')
            for title in characterTitles:
                characterTitle.append((title.text.split(',')[0]).replace('\xa0', ''))
        except:
            characterTitle = ''
        try:
            characterMeasure = []
            characterMeasures = card.find('div', class_='card__tabs tabs').find_all('span', class_='character__label')
            for measure in characterMeasures:
                meas = measure.text.split(',')[-1].replace('\xa0', '')
                if (len(meas) <= 5):
                    characterMeasure.append(meas)
                else:
                    characterMeasure.append('')
        except:
            characterMeasure = ''
        try:
            characterValue = []
            characterValues = card.find('div', class_='card__tabs tabs').find_all('span', class_='character__value')
            for value in characterValues:
                characterValue.append(value.text.split(','))
        except:
            characterValue = ''

        data = {'title': title,
                'photo': photo,
                'price': price,
                'currency': currency,
                'description': description,
                'characterTitle': characterTitle,
                'characterMeasure': characterMeasure,
                'characterValue': characterValue}


        write_csv(data)


def write_csv(data):
    characters = []
    for i in range(len((data['characterTitle'])) - 1):
        characters.extend((data['characterTitle'][i], data['characterMeasure'][i], data['characterValue'][i][0]))
    with open('snopTerm2.csv', 'a', newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow((data['title'], data['photo'], data['price'], data['currency'], data['description'], characters))
        # writer.writerow(data['title'], 'dsfsdfs')




def main():
    url = 'https://snol-term.ru/products/'
    pages = 5

    for i in range(pages):
        get_link_cards(get_html(url+'?page='+repr(i+1)))

    get_information_card()

if __name__ == '__main__':
    main()