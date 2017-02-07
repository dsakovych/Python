import requests
import re
import time
import csv
from bs4 import BeautifulSoup
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36'
                         ' (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


def imdb_year_url(year):
    year = str(year)
    return 'http://www.imdb.com/search/title?year=%s,%s&title_type=feature&sort=moviemeter,asc' % (year, year)


def find_next_page(soup):
    try:
        return 'http://www.imdb.com/search/title' + soup.find('a', {'class': 'lister-page-next next-page'}).get('href')
    except AttributeError:
        return False


def make_soup(url):
    return BeautifulSoup(requests.get(url, headers=headers).content, 'lxml')


def main():
    url = imdb_year_url(2000)
    print('Starting gathering films urls for year 2000:')
    print('parsing ' + url)
    soup = make_soup(url)
    counter = 0
    while True:
        heads = soup.findAll("h3")
        data = {}
        for item in heads:
            try:
                if 'title' in item.find('a').get('href'):
                    data[item.find('a').get_text()] = 'http://www.imdb.com' + item.find('a').get('href')
            except AttributeError:
                continue
        counter += len(data)
        with open('data.csv', 'a', encoding='utf8') as file:
            w = csv.writer(file, delimiter='|', lineterminator='\n')
            w.writerows(data.items())
        print('%d films were gathered and written to data.csv' % counter)
        if find_next_page(soup):
            print('parsing ' + find_next_page(soup))
            soup = make_soup(find_next_page(soup))
        else:
            break
        time.sleep(2)

    print('\nFINISHED!')


if __name__ == '__main__':
    main()
