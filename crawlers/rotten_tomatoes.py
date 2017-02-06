import requests
from bs4 import BeautifulSoup
import re
import codecs

def get_soup(link):
    html = requests.get(link)
    soup = BeautifulSoup(html.text, "lxml")
    return soup

# few ids for demo purpose
ids = ['tom_and_huck', '1018047-sabrina', '1068470-sudden_death', 'war_on_everyone']
source = "https://www.rottentomatoes.com/m/{}/reviews/"

for rt_id in ids:
    soup = get_soup(source.format(rt_id))
    movie_title = soup.find('div', {'class':'bottom_divider'}).parent.find('h2').a.string
    
    for review_container in soup.findAll("div", {"class":"col-xs-16 review_container"}):
        classes = review_container.findAll('div', recursive=False)[0]['class']
        is_rotten = 'rotten' in classes
        is_fresh = 'fresh' in classes
        
        if not is_rotten and not is_fresh:
            print('that\'s weird! can\'t understand the rating. RT ID is :' + rt_id)
            continue
        
        the_review = review_container.find('div', {"class":"the_review"})
        text = the_review.string
        
        if not text.strip():
            continue
        
        # append to the end of file
        with codecs.open('reviews.tsv', 'a+', 'utf-8') as myfile:
            myfile.write(u'{}\t{}\t{}\n'.format(movie_title, text, 1 if is_fresh else 0))
