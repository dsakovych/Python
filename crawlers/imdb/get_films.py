import requests
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
    years = [str(x) for x in range(2000, 2018)]

    for year in years[1:2]:  # change to get all years
        url = imdb_year_url(year)
        start_time = time.time()
        print('Starting gathering films urls for year %s:' % year)
        print('parsing ' + url)
        soup = make_soup(url)
        counter = 3825  # year 2000 ended on 3825
        while True:
            heads = soup.findAll("h3")
            data = []
            for item in heads:
                try:
                    if 'title' in item.find('a').get('href'):
                        counter += 1
                        data.append((item.find('a').get_text(),
                                    ('http://www.imdb.com' + item.find('a').get('href')).replace('?ref_=adv_li_tt', ''),
                                     year, counter)
                                    )
                        #data[item.find('a').get_text()] = ('http://www.imdb.com' + item.find('a').get('href')).replace('?ref_=adv_li_tt', '')
                except AttributeError:
                    continue
            with open('films/' + year + '.csv', 'a', encoding='utf8') as file:
                w = csv.writer(file, delimiter='|', lineterminator='\n')
                to_write = data
                w.writerows(to_write)
            print('%d films were gathered and written to %s.csv' % (counter, year))
            if find_next_page(soup):
                print('parsing ' + find_next_page(soup))
                soup = make_soup(find_next_page(soup))
            else:
                break
            time.sleep(2)  # we're not robots, we're just consistent humans :-)

        print('\n Year %s is FINISHED!' % year)
        print('Time spent : %s' % str(time.time() - start_time))


if __name__ == '__main__':
    main()
