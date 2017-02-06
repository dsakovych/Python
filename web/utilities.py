import csv
import re
import requests
from bs4 import BeautifulSoup, Comment
import textwrap

from config import APP_DIR
from app import logger
from urllib.parse import unquote
##################################################################
##################################################################

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36'
                         ' (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

bad_status_codes = [400, 401, 403, 404, 500, 501, 502, 503, None]
bad_endings = ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'rtf', 'pdf', 'txt', 'jpg', 'png', 'gif']

special_sites = dict()
with open(APP_DIR + '/app/data/' + 'robms_domains_list.csv', 'r') as csvfile:
    temp = csv.reader(csvfile, delimiter=',')
    for row in temp:
        special_sites[row[0]] = row[1]

excluded_sites = list()
with open(APP_DIR + '/app/data/' + 'exclude_domains.txt', 'r') as file:
    for row in file:
        excluded_sites.append(row.strip())
##################################################################
##################################################################


def request_status(url):
    try:
        return requests.get(url, timeout=5).status_code
    except requests.exceptions.RequestException:
        return None


def home_page(inp_url):
    inp_url = inp_url.replace('http://', '').replace('https://', '')
    if inp_url.find('/') != -1:
        inp_url = inp_url[:inp_url.find('/')]
    if inp_url.find('%') != -1:
        inp_url = inp_url[:inp_url.find('%')]
    return 'http://' + inp_url


def clean_bad_endings(lst):
    results = map(lambda x: x if x.rstrip().rsplit('.', 1)[1] not in bad_endings else None, lst)
    results = list(filter(None, results))
    results = list(set(results))
    return results


def un_quote(url):
    while url.find('%') != -1:
        url = unquote(url)
    return url


def excluded_url(url):
    """ check is url is present in *excluded_sites*

    :param url: url
    :return: bool
    """
    if url is None:
        return True
    for item in excluded_sites:
        if item in url:
            return True
    return False


def correct_url(url):
    """Checks if input is real working url. Includes several approaches to optimize time execution

    :param url: string
    :return: bool
    """

    def is_ascii(s):
        return all(ord(c) < 128 for c in s)

    if url is None:
        return None
    url = str(url)
    if not is_ascii(url):
        return None
    elif url.replace('.', '').replace('-', '').isdigit():
        return None

    url = url.replace('https://', '').replace('http://', '').replace('www.', '')
    url_www = 'http://www.' + url
    url_wo_www = 'http://' + url
    try:
        requests.get(url_wo_www, timeout=5)
        return url_wo_www
    except requests.exceptions.RequestException:
        try:
            requests.get(url_www, timeout=5)
            return url_www
        except requests.exceptions.RequestException:
            return None


def url_prettified(inp_url):
    if inp_url is None:
        return None

    inp_url = inp_url.replace('http://', '').replace('https://', '').replace('www.', '')
    if inp_url.find('/') != -1:
        inp_url = inp_url[:inp_url.find('/')]
    if inp_url.find('%') != -1:
        inp_url = inp_url[:inp_url.find('%')]
    return inp_url
##################################################################
##################################################################


def justify(text, width=100):
    """ justifying text by width

    :param text: string
    :param width: width
    :return: new string
    """
    lines = textwrap.wrap(text, width, break_on_hyphens=False)

    def line_justify(line):
        n_gp = line.count(' ')
        if n_gp == 0:
            return line
        n_sp = width - len(line) + n_gp
        n_sp_a, n_sp_b = divmod(n_sp, n_gp)
        _line_ = ''
        words = line.split()
        for i, word in enumerate(line.split()[:-1]):
            _line_ += word + ' ' * (n_sp_a + (i < n_sp_b))
        return _line_ + words[-1]

    return '\n'.join(list(map(line_justify, lines[:-1])) + [lines[-1], ])


class SiteParser:
    """ This is a web-site object. Allows to work with web-site layout and extract required information from it.
    **Requires**: BeautifulSoup, re, requests
    """

    def __init__(self, input_url):
        """ In this method we define our ``input_url`` as a new object.
        Page is processed by ``BeautifulSoup``, all tags and javascript are removed, only flat text is remained.
        :param input_url: Input url
        :type input_url: str
        Example:
            >>> site = SiteParser('http://b2bsky.co.ua/info/37883328')
        """

        html = requests.get(input_url, headers=headers, timeout=5).content
        soup = BeautifulSoup(html, "lxml")

        #: Original BeautifulSoup content
        self.soup = soup
        #: Cleaned site content presented as a string.
        self.content = self.get_soup_content()
        #: Current rank of web-site object. By default set to 0.4
        self.rank = 0.4
        #: Input url of the object
        self.url = input_url
        #: Site is in the list of ``special_sites`` and its rank was increased or decreased
        self.is_special = False
        #: **ein** was already found for this object (optimizing parsing time)
        self.ein_present = False

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

    def get_soup_content(self):
        """ Constructor's method that extracts and cleans web-site content

        :return:
        """

        def remove_dubl(seq):
            seen = set()
            seen_add = seen.add
            return [x for x in seq if not (x in seen or seen_add(x))]

        [s.extract() for s in self.soup('script')]
        [s.extract() for s in self.soup('style')]

        for element in self.soup(text=lambda text: isinstance(text, Comment)):
            element.extract()

        text = self.soup.getText(separator=u'\n')
        text = list(filter(None, text.split('\n')))
        text = [x.strip().lower() for x in text]
        text = remove_dubl(text)
        return ' '.join(text)

    def find_ein(self, number, region):
        """Method looks for EIN number (8 or 10 digits).
        If ``number`` is found, prints about it and return ``True``, otherwise doesn't print nothing and return ``False``
        :param number: searched EIN number
        :type number: str
        :param region: 'uk' or 'ru'
        :type region: str
        :return: boolean
        Example:
            >>> site.find_ein('37883328', 'uk')
            EDRPOU Number 37883328 was found on  http://b2bsky.co.ua/info/37883328
        """

        if number is None or len(number) == 0:
            return False

        if self.ein_present:
            return True

        number = str(number).lower()
        if region == 'ru':
            re_find = re.compile(".*?(\d{10})")
        else:
            re_find = re.compile(".*?(\d{8})")
        reg_find = re.findall(re_find, self.content)
        if reg_find:
            for item in reg_find:
                if item == number:
                    msg = 'EDRPOU Number ' + number + ' was found on ' + self.url
                    logger.warning(msg)
                    del msg
                    self.ein_present = True
                    return True
        return False

    def find_word(self, inp_words):
        """Method looks for word(s) that represented as string.
        If ``inp_words`` is found, prints about it and return ``True``, otherwise doesn't print nothing and return ``False``
        :param inp_words: searched word(s)
        :type inp_words: str
        :return: boolean
        Example:
            >>> site.find_word('Мечникова')
            Words "м е ч н и к о в а" was found on http://b2bsky.co.ua/info/37883328
        """
        if inp_words is None or len(inp_words.strip()) == 0:
            return False

        inp_words = str(inp_words).lower()
        if inp_words in self.content:
            msg = '''Words "''' + inp_words + '''" was found on ''' + self.url
            logger.warning(msg)
            del msg
            return True
        return False

    def find_phone_number(self, number):
        """Method looks for ``number`` that represented as a string.
        If ``number`` is found, prints about it and return ``True``,
        otherwise doesn't print nothing and return ``False``
        This method differs from :func:`find_phone_numbers` as it looks throw all layout,
        not just ``synonyms_words``, and finds first coincidence.
        :param inp_words: searched word(s)
        :type inp_words: str
        :return: boolean
        Example:
            >>> site.find_phone_number('443931071')
            Number 0443931071 was found on http://b2bsky.co.ua/info/37883328
        """
        if number is None or len(number.strip()):
            return False

        re_num = re.compile('.*?(\d{1,3})[-\ (]*(\d{2,5})[-\ )]*(\d{1,4})[-\ ]*(\d{1,4})[-\ ]*(\d{0,4})')
        number = str(number).replace('-', '').replace(' ', '').replace(')', '').replace('(', '').replace(
                    '/', '').replace('.', '').replace('\/', '').lower()
        last_five_digit = number[len(number) - 5:]
        matches = re.findall(re_num, self.content)
        if matches:
            numbers = [''.join(list(item)) for item in matches]
            numbers = list(set(numbers))
            for item in numbers:
                if last_five_digit in str(item):
                    msg = '''Number "''' + number + '''" was found on ''' + self.url
                    logger.warning(msg)
                    del msg
                    return True
        return False

    def all_phone_numbers(self):
        """ finds all objects similar to phone number structure due to regex

        :return: list
        """

        re_num = re.compile('.*?(\d{1,3})[-\ (]*(\d{2,5})[-\ )]*(\d{1,4})[-\ ]*(\d{1,4})[-\ ]*(\d{0,4})')
        matches = re.findall(re_num, self.content)
        if matches:
            numbers = [''.join(list(item)) for item in matches]
            return list(set(numbers))

    def find_email(self):
        """Looks through the page text for e-mails and return list of their domain names
        :return: list - list of web-sites
        Example:
            >>> site = SiteParser('http://www.promelectro.biznes-pro.ua/ru/')
            >>> site.find_email()
            ['promelectro.com']
        """
        regex_email = re.compile(".*?[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,6})")
        emails = re.findall(regex_email, self.content)
        if emails:
            return list(set(emails))

    def all_urls(self):
        """Returns list of objects similar by their structure to web-site due to regex. All returned urls are ALREADY
            filtered by :func:`excluded_url`, :func:`clean_bad_endings` and :func:`correct_url`
        :return: list
        Example:
            >>> site = SiteParser('http://www.promelectro.biznes-pro.ua/ru/')
            >>> site.all_urls()
            ['http://promelectro.com']
        """

        regex_site = re.compile("([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?")
        sites = re.findall(regex_site, self.content)
        if sites:
            sites = [''.join(list(item[0])) for item in sites]
            sites = [x for x in sites if not excluded_url(x)]
            sites = clean_bad_endings(sites)
            sites = set(map(lambda x: x.replace('www.', ''), sites))
            sites = list(filter(None, list(map(correct_url, sites))))
            return sites
        return []


def url_contacts(inp_url):
    """Parses page layout and returns a link to 'Contacts' page.
    The search is performed by words that are listed in ``contacts_synonyms``.
    If it didn't work looks through all *href* listed in ``contacts_hrefs`` and returns first matched result.
    If nothing found returns ``None``
    **Requires**: BeautifulSoup, re, requests
    :param inp_url: Input url
    :type inp_url: str
    :return: str - link on page with contact information
    Example:
        >>> url_contacts('http://kasagrohim.com/')
        http://kasagrohim.com/contaktu/
    """

    if inp_url is None:
        return None

    def prettify(link):
        return link.replace('https://', '').replace('http://', '').replace(
                            '///', '/').replace('//', '/')
    try:
        page = requests.get(inp_url, headers=headers, timeout=5)
    except requests.exceptions.RequestException:
        return None
    html = page.content
    soup = BeautifulSoup(html, "lxml")
    contacts_synonyms = ['Контакты', 'контакты', 'КОНТАКТЫ', 'Contacts', 'contacts', 'CONTACTS',
                         'Контакти', 'контакти', 'КОНТАКТИ', 'Контакт', 'контакт', 'КОНТАКТ',
                         'Contact', 'contact', 'CONTACT',
                         'О нас', 'Про нас', 'About'
                         ]
    contacts_hrefs = ['contact', 'kontakt', 'contakt', 'kontact']

    for word in contacts_synonyms:
        for elem in soup(text=re.compile(word)):
            ololo = elem.parent
            if ololo.get('href') is None:
                tmp = ololo.parent.get('href')
            elif '#' in ololo.get('href'):
                tmp = None
            else:
                tmp = ololo.get('href')
            if tmp is not None:
                if 'http' in tmp:
                    result = prettify(tmp)
                    return 'http://' + result
                else:
                    result = home_page(inp_url) + '/' + tmp
                    result = prettify(result)
                    return 'http://' + result
    for word in contacts_hrefs:
        for elem in soup(href=re.compile(word)):
            tmp = elem.get('href')
            if 'http' in tmp:
                result = prettify(tmp)
                return 'http://' + result
            else:
                result = home_page(inp_url) + '/' + tmp
                result = prettify(result)
                return 'http://' + result
    return None


