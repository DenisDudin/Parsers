import csv

import requests
from bs4 import BeautifulSoup

def write_csv(data):
    with open('avito.csv', 'a', newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow((data['title'], data['price'], data['geo'], data['date']))

def get_html(url):
    r = requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')

    pages = soup.find('div', class_='pagination-root-Ntd_O').find_all('span', class_='pagination-item-JJq_j')[-2].get('data-marker')
    total_pages = pages.split('(')[1].split(')')[0]
    return int(total_pages)

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='items-items-kAJAg').find_all('div', class_='iva-item-content-UnQQ4')

    for ad in ads:
        #Для отсеивания из выдачи товаров, не имеющих в названии требуемое
        # name = ad.find('div', class_='iva-item-body-R_Q9c').find('a', class_='link-link-MbQDP').text.strip()
        # if 'товар' in name:
        try:
            title = ad.find('div', class_='iva-item-body-R_Q9c').find('a', class_='link-link-MbQDP').text.strip()
        except:
            title = ''
        try:
            price = ad.find('div', class_='iva-item-priceStep-QN8Kl').text.strip()
        except:
            price = ''
        try:
            geo = ad.find('div', class_='geo-root-H3eWU').text.strip()
        except:
            geo = ''
        try:
            date = ad.find('div', class_='date-root-QeIIB').text.strip()
        except:
            date = ''


        data = {'title': title,
                'price': price,
                'geo': geo,
                'date': date}

        write_csv(data)

def main():
    url = 'https://www.avito.ru/rossiya/zapchasti_i_aksessuary?p=5&q=манометр'
    base_url = 'https://www.avito.ru/rossiya/zapchasti_i_aksessuary?'
    page_part = 'p='
    query_part = '&q=манометр'

    total_pages = get_total_pages(get_html(url))
    for i in range(1, 2):
        url_gen = base_url + page_part + str(i) + query_part
        html = get_html(url_gen)
        get_page_data(html)


if __name__ == '__main__':
    main()