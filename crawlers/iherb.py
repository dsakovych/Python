import requests
from bs4 import BeautifulSoup
import re
def get_soup(link):
    html = requests.get(link)
    soup = BeautifulSoup(html.text, "lxml")
    return soup
def parse(soup):
    r = []
    for review in soup.findAll("div", {"class": "row review-row"}):
        r.append([str(review.find("a", {"class": "stars"}).i)[21],
                  review.find("div", {"class": "textcontainer"}).bdi.p.text])
    return r
def preprocess(text):
    return text.replace("|", ";").replace("\r", '').replace("\n", '')
def save(reviews):
    with open("reviews_iherb.csv", "a") as f:
        for review in reviews:
            f.write(review[0] + "|" + preprocess(review[1]) + "|http://www.iherb.com\n")
n_pages = 71
source = "http://www.iherb.com/Supplements?p={}&noi=192&disc=true"
products_list = []
for i in range(1, n_pages+1):
    soup = get_soup(source.format(i))
    for item in soup.findAll("div", {"class":"product ga-product col-xs-12 col-sm-12 col-md-8 col-lg-6"}):
        products_list.append(item.a["href"].replace("/pr/", "/r/"))
product_source = "{}/?p={}&revl=en"
for s in products_list:
    print(s)
    soup = get_soup(product_source.format(s, 1))
    total = int(re.search(r"(\d+) total", str(soup.find("p", {"class": "display-items-L"}))).group(1))
    r = []
    r.extend(parse(soup))
    for p in range(2, total // 10 + (total % 10 > 0) + 1):
        soup = get_soup(product_source.format(s, p))
        r.extend(parse(soup))
    save(r)
