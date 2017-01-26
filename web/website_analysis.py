# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup, Comment

def get_url_content(url):

    def remove_dubl(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    html = requests.get(url, headers=headers, timeout=7).content
    soup = BeautifulSoup(html, "lxml")

    [s.extract() for s in soup('script')]
    [s.extract() for s in soup('style')]

    for element in soup(text=lambda text: isinstance(text, Comment)):
        element.extract()

    text = soup.getText(separator=u'\n')
    text = list(filter(None, text.split('\n')))
    text = [x.strip() for x in text]
    text = remove_dubl(text)
    # text = ' '.join(text)
    # text_short = [x for x in text if len(x) > 2]
    # text = text.encode('utf-16-le').decode('cp1251').replace('\x00', '')
    # return ' '.join(text_short)
    return '\n'.join(text)
