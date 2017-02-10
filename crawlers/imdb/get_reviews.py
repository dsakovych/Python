import pandas as pd
from get_films import make_soup
import csv
import time
import random


def get_reviews_num(input):
    try:
        return int(make_soup(input).find('td', {'align': 'right'}).get_text().split(' ')[0])
    except (IndexError, AttributeError):
        return 0


def gather_reviews(id, name, input_url):

    input_url += 'reviews'
    reviews_pages = int(get_reviews_num(input_url) / 10) if get_reviews_num(input_url) % 10 == 0 else int(
                        get_reviews_num(input_url) / 10) + 1

    df = pd.DataFrame()
    print('Starting gathering reviews for "%s". Total number of reviews is %d' % (name, get_reviews_num(input_url)))
    for i in range(reviews_pages):
        page = input_url + '?start=' + str(i * 10)
        print('Parsing: %s' %page)
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

    df = df.reset_index()
    df = df.ix[:, ['name', 'rate', 'title', 'review']]
    df.to_csv('reviews/' + id + '.csv', sep='|', index='False')
    print('Done! All reviews were written to file "%s"' % str(id + '.csv'))


def main():
    years = [str(x) for x in range(2000, 2018)]
    for year in years[:1]:
        with open('films/' + year + '.csv') as file:
            line_reader = csv.reader(file, delimiter='|')
            for row in line_reader:
                gather_reviews(row[3], row[0], row[1])
                pause = random.randint(10, 30)
                print('*************************')
                print('pause: %d seconds' % pause)
                print('*************************')
                time.sleep(pause)  # at least we are trying to be polite


if __name__ == '__main__':
    main()
