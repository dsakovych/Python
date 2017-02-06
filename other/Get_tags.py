# -*- coding: utf8 -*-

#just retrieve all tags 
from bs4 import BeautifulSoup as BeautifulSoup1
import requests
import re

url = ["http://agropartner.info/"]
for line in url:
    print "Here is tags from: " + line
    page = requests.get( line )
    html = page.content
    soup = BeautifulSoup1(html)
    tags_all = []

    temp = soup.prettify().split("\n")

    for line in temp:
        line = line.strip().encode('utf8')
        if re.search("^<([a-z]+) .+",line):
            tag = re.findall("^<([a-z]+) .+",line)[0]
            if tag not in tags_all:
                tags_all.append(str(tag))
                print tag
            else: continue
