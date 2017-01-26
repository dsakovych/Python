# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup, Comment

special_sites = dict()

######################################################################
######################################################################

class SiteParser:

    def __init__(self, input_url):

        html = requests.get(input_url, headers=headers, timeout=10).content
        soup = BeautifulSoup(html, "lxml")
        content = get_url_content(input_url)

        #: Original BeautifulSoup content
        self.html = soup
        #: List of strings of website content w/o tags and mostly w/o javascript.
        self.content = content
        #: Current rank of web-site object. By default set to 0.4
        self.rank = 0.4
        #: Input url of the object
        self.url = input_url
        #: Site is in the list of ``restricted_sites`` and its rank was increased or decreased
        self.is_special = False

        for item in special_sites.items():
            if item[0] in input_url:
                self.is_special = True
                if item[1] == str(5):
                    self.rank -= 0.2
                elif item[1] == str(4):
                    self.rank += 0.1
                else:
                    self.rank += 0.2
                break

    #: Name of the object
    name = None

    def find_ein(self, number, region):

        if number is None:
            return False
        temp_lst = []
        if region == 'ru':
            re_find = re.compile("^.*?(\d{10}).*")
        else:
            re_find = re.compile("^.*?(\d{8}).*")
        for line in self.soup:
            reg_find = re.findall(re_find, line)
            if reg_find:
                temp_lst.extend(reg_find)
        if number in temp_lst:
            text = 'EDRPOU Number ' + number + ' was found on ' + self.url
            logger.warning(text)
            del text
            return True
        else:
            return False

    def find_word(self, inp_words):

        if len(inp_words) < 1:
            return False
        try:
            result_lines = []
            key_words = inp_words.lower()
            for line in self.soup:
                line = str(line).strip().lower()
                if key_words in line:
                    if line not in result_lines:
                        result_lines.append(line)
            if len(result_lines) > 0:
                text = '''Words "''' + ' '.join(inp_words) + '''" was found on ''' + self.url
                logger.warning(text)
                del text
                return True
        except:
            text = '''*** WORD SEARCH ERROR "''' + ' '.join(inp_words) + '''". URL: ''' + self.url + " REASON: " + \
                   str(sys.exc_info()[1])
            logger.warning(text)
            del text
            return False
        return False

    def find_phone_number(self, number):

        re_num = re.compile('.*?(\d{1,3})[-/\. (]*(\d{2,5})[-/\. )]*(\d{1,4})[-/\. ]*(\d{1,4})[-/\. ]*(\d{0,4})')
        try:
            number = number.replace('-', '')
            number = number.replace(' ', '')
            number = number.replace(')', '')
            number = number.replace('/', '')
            number = number.replace('\/', '')
            number = number.replace('(', '')
            number = number.replace('.', '')
            last_five_digit = number[len(number) - 5:]
            numbers = []
            for line in self.soup:
                matches = re.findall(re_num, line)
                if re.findall(re_num, line):
                    numbers.extend([''.join(list(item)) for item in matches])
            numbers = list(set(numbers))
            for item in numbers:
                if last_five_digit in str(item):
                    text = '''Number "''' + str(item) + '''" was found on ''' + self.url
                    logger.warning(text)
                    del text
                    return True
        except:
            text = '''*** NUMBER SEARCH ERROR "''' + number + '''". URL: ''' + self.url + " REASON: " + \
                   str(sys.exc_info()[1])
            logger.warning(text)
            del text
            return False
        return False

    def find_email(self):

        regex_email = re.compile(".*[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,6}).*")
        email_result = []
        for line in self.html:
            line = str(line).strip().lower()
            email_temp = re.findall(regex_email, line)
            if len(email_temp) > 0:
                for url in email_temp:
                    if 'www' in url:
                        url_1 = url[url.find('www'):]
                        url_2 = url[:url.find('www')]
                        email_result.append(url_1)
                        email_result.append(url_2)
                    else:
                        email_result.append(url)
        return email_result

    def find_site(self):

        site_synonyms = ['Веб-страница', 'Веб-сторінка', 'Веб', 'Сайт', 'WWW', 'страница', 'сторінка', 'Website', 'website']
        try:
            reg_site = re.compile('.*www.([0-9A-Za-z.-]+)')
            reg_site1 = re.compile('.*http://([0-9A-Za-z.-]+)')
            for word in site_synonyms:
                for elem in self.html(text=re.compile(word)):
                    for i in range(1, 4):
                        site = re.findall(reg_site, str(elem))
                        site1 = re.findall(reg_site1, str(elem))
                        if site:
                            return 'http://' + site[0]
                        elif site1:
                            return 'http://' + site1[0]
                        else:
                            elem = elem.previous
                    for i in range(1, 4):
                        site = re.findall(reg_site, str(elem))
                        site1 = re.findall(reg_site1, str(elem))
                        if site:
                            return 'http://' + site[0]
                        elif site1:
                            return 'http://' + site1[0]
                        else:
                            elem = elem.parent
        except:
            return None

######################################################################
######################################################################

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
