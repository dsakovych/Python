from googleapiclient.discovery import build
import googlemaps

GOOGLE_API_KEY = 'AIzaSyAFPCS7ZIsOFWj2KelQmwbM3j-Wgkef59o'
google_search_engine_id_uk = '012932533370143995153:gtohipjd2fa'
google_search_engine_id_ru = '012932533370143995153:-zfqgrrwrtk'
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
service = build('translate', 'v2', developerKey=GOOGLE_API_KEY)


#########################################################################
############################### TRANSLATE ###############################

def translate(target, word, source=None):
    """Google translate API function
            Translates ``word`` to ``target`` language.
            :param target: language translate to
            :type target: str
            :param word: what to translate
            :type word: str
            :param source: source language
            :type source: str
            :return: str
            Example:
                >>> translate('en', 'заяц')
                hare
            """
    return service.translations().list(target=target,
                                       q=word,
                                       source=source).execute()['translations'][0]['translatedText']


#########################################################################
############################### ADDRESS #################################

def just_street(street):
    street = street.lower()
    lst = ['бульвар', 'б.', 'вулиця', 'улица', 'вул.', 'ул.', 'проспект', 'пр.', 'просп.',
           'провулок', 'переулок', 'пров.', 'пер.', 'шосе', 'шоссе', 'Ulitsa', 'ulitsa']
    for item in lst:
        if item in street:
            street = street.replace(item, '').strip()
    return street


def get_address(city, address):
    """
    :param city:
    :param address:
    :return: json
                Example:
                >>> get_address('Черкаси', 'просп. Хіміків 74')
                {'street_number': '74', 'source': {'address': {'uk': 'просп. Хіміків 74', 'en': '',
                'ru': 'просп. химиков 74'}, 'city': {'uk': 'Черкаси', 'en': '', 'ru': 'Черкассы'},
                'street': {'uk': 'Хіміків', 'en': '', 'ru': 'химиков'}},
                'translate': {'address': {'uk': 'хіміків проспект', 'en': 'Khimikiv Avenue', 'ru': 'Химиков проспект'},
                'city': {'uk': 'Черкаси', 'en': 'Cherkasy', 'ru': 'Черкассы'}, 'street': {'uk': 'хіміків', 'en': '',
                'ru': 'химиков'}}}
    """
    address = address.split(',')[0]
    full_address = city + ',' + address
    geocode_result = gmaps.geocode(full_address)

    data = {'source': {'city': {'uk': '', 'ru': '', 'en': ''}, 'address': {'uk': '', 'ru': '', 'en': ''},
                       'street': {'uk': '', 'ru': '', 'en': ''}},
            'translate': {'city': {'uk': '', 'ru': '', 'en': ''}, 'address': {'uk': '', 'ru': '', 'en': ''},
                          'street': {'uk': '', 'ru': '', 'en': ''}},
            'street_number': ''}
    try:
        results = geocode_result[0]['address_components']
        for res in results:
            if res['types'][0] == 'street_number':
                data['street_number'] = res['long_name']
            if res['types'][0] == 'route':
                data['translate']['address']['en'] = res['long_name']
            if res['types'][0] == 'locality':
                data['translate']['city']['en'] = res['long_name']

        data['translate']['city']['uk'] = translate('uk', data['translate']['city']['en'], 'en')
        data['translate']['city']['ru'] = translate('ru', data['translate']['city']['en'], 'en')
        data['translate']['address']['uk'] = translate('uk', data['translate']['address']['en'], 'en')
        data['translate']['address']['ru'] = translate('ru', data['translate']['address']['en'], 'en')
        data['translate']['street']['uk'] = just_street(data['translate']['address']['uk'])
        data['translate']['street']['ru'] = just_street(data['translate']['address']['ru'])

    except:
        data['translate']['city']['uk'] = translate('uk', city)
        data['translate']['city']['ru'] = translate('ru', city)
        data['translate']['address']['uk'] = translate('uk', address)
        data['translate']['address']['ru'] = translate('ru', address)
        data['translate']['street']['uk'] = just_street(data['translate']['address']['uk'])
        data['translate']['street']['ru'] = just_street(data['translate']['address']['ru'])

    data['source']['city']['uk'] = translate('uk', city)
    data['source']['city']['ru'] = translate('ru', city)
    data['source']['address']['uk'] = translate('uk', address)
    data['source']['address']['ru'] = translate('ru', address)
    data['source']['street']['uk'] = ' '.join(data['source']['address']['uk'].split()[1:]).replace(
        data['street_number'], '').strip()
    data['source']['street']['ru'] = ' '.join(data['source']['address']['ru'].split()[1:]).replace(
        data['street_number'], '').strip()

    return data


#########################################################################
############################### SEARCH ##################################

def google_search(query, engine):
    """Function runs Google custom search using key words
                    Method makes request to Google custom search and returns search results on requested item
                    :param query: search item (phrase)
                    :type query: str
                    :param engine: type of search engine (*ru* or *uk*)
                    :type engine: str
                    :return: list
                    """
    results = []
    query = '+'.join(query.split(' '))
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    if engine == 'ru':
        engine_setup = google_search_engine_id_ru
    else:
        engine_setup = google_search_engine_id_uk

    for i in range(2):
        res = service.cse().list(q=query, start=i * 10 + 1, cx=engine_setup).execute()
        try:
            results.extend([res['items'][i]['link'] for i in range(len(res['items']))])
        except:
            pass
    results = list(set(results))
    return results
