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


def main():
    url = 'http://www.imdb.com/title/tt0204946/?ref_=adv_li_tt'
    url1 = 'http://www.imdb.com/title/tt0215941/?ref_=adv_li_tt'
    url2 = 'http://www.imdb.com/title/tt0266802/?ref_=adv_li_tt'
    soup = make_soup(url1)
    try:
        text = soup(text=re.compile('user reviews'))[0].parent.get('href')
        print('http://www.imdb.com/' + text)
    except IndexError:
        print('ololo')


def gather_reviews():
    url = 'http://www.imdb.com//title/tt0215941/reviews?start=0'
    #url = 'http://www.imdb.com/title/tt0204946/reviews?ref_=tt_ov_rt'
    soup_rates = make_soup(url).findAll('h2')
    reviews_num = make_soup(url).find('td', {'align': 'right'}).get_text()
    rates = []
    for item in soup_rates:
        title = item.next
        rate = item.next.next.next.get('alt') if item.next.next.next.get('alt') is not None else 'nan'
        rates.append((title, rate))
    soup_reviews = make_soup(url).findAll('div', {'class': 'yn'})
    #print(len(soup_reviews))
    reviews = []
    for item in soup_reviews:
        reviews.append(item.previous.previous)
        #print(item.previous.previous)
    results = list(zip(rates, reviews))
    print(reviews_num)



if __name__ == '__main__':
    #main()
    gather_reviews()
