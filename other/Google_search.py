# retrieve links from Google querry and write in to txt file. Search parameters can be customized by reading Google Web Search API

import requests
import urllib
from bs4 import BeautifulSoup as BS
import re

sites = []

string = raw_input("Enter your request: ")

def google_request(string):
    lst = string.split()
    return "https://www.google.com/search?" + "start=0" + "&num=10" + "&q="+"+".join(lst)

page = requests.get( google_request(string) )
html = page.content
soup = BS(html)

print google_request(string)

sites_file = open("Sites.txt", "w") 

temp = soup.prettify().split('\n')

for line in temp:
    line = line.strip()
    if re.search('^<a href="[/]url[?]q=.+',line):
        url = re.findall('^<a href="/url[?]q=(.+?)&amp',line)[0]
        while(url.find('%') != -1):
            url = urllib.unquote(url)
        sites_file.write(url+"\n")
        sites.append(url)

sites_file.close()

for site in sites:
    print site
