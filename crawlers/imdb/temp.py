import requests
import re
import time
import csv
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36'
                         ' (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


def make_soup(url):
    return BeautifulSoup(requests.get(url, headers=headers).content, 'lxml')


def get_reviews_num(input):
    try:
        return int(make_soup(input).find('td', {'align': 'right'}).get_text().split(' ')[0])
    except IndexError:
        return 0


def gather_reviews(id, name, input_url):
    input_url = input_url + '/reviews'

    reviews_pages = int(get_reviews_num(input_url) / 10) if get_reviews_num(input_url) % 10 == 0 else int(
        get_reviews_num(input_url) / 10) + 1

    df = pd.DataFrame()
    print(reviews_pages)
    for i in range(1):
        page = input_url + '?start=' + str(i * 10)
        print(page)
        soup_rates = make_soup(page).findAll('h2')
        soup_reviews = make_soup(page).findAll('div', {'class': 'yn'})
        rates = []
        for item in soup_rates:
            title = item.next.replace('|', '')
            rate = item.next.next.next.get('alt') if item.next.next.next.get('alt') is not None else 'nan'
            rates.append((title, rate))
        reviews = []
        for item in soup_reviews:
            reviews.append(item.previousSibling.previousSibling.get_text().replace('\n', '').replace('|', ''))
        results = list(zip(rates, reviews))
        for item in results:
            df = df.append([{'name': name, 'title': item[0][0], 'rate': item[0][1], 'review': item[1]}])

        df = df.ix[:, ['name', 'rate', 'title', 'review']]
        df.to_csv(id + '.csv', sep='|', quotechar='"', index='False')


if __name__ == '__main__':
    url = 'http://www.imdb.com//title/tt0215941'
    url1 = 'http://www.imdb.com//title/tt0195714'
    name = 'Unbreakable'
    gather_reviews(name, url1)
