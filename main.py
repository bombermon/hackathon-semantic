from bs4 import BeautifulSoup
import requests as req
import re
from SPARQLWrapper import SPARQLWrapper, JSON
from fake_useragent import UserAgent
import wikipedia

'''
Берем значит ссылку и через семантик веб анализируем человек это или не человек имя это или не имя 
'''


def get_wiki_url(wikidata_id, lang='en', debug=False):
    import requests
    from requests import utils

    url = (
        'https://www.wikidata.org/w/api.php'
        '?action=wbgetentities'
        '&props=sitelinks/urls'
        f'&ids={wikidata_id}'
        '&format=json')
    json_response = requests.get(url).json()
    if debug: print(wikidata_id, url, json_response)

    entities = json_response.get('entities')
    if entities:
        entity = entities.get(wikidata_id)
        if entity:
            sitelinks = entity.get('sitelinks')
            if sitelinks:
                if lang:
                    # filter only the specified language
                    sitelink = sitelinks.get(f'{lang}wiki')
                    if sitelink:
                        wiki_url = sitelink.get('url')
                        if wiki_url:
                            return requests.utils.unquote(wiki_url)
                else:
                    # return all of the urls
                    wiki_urls = {}
                    for key, sitelink in sitelinks.items():
                        wiki_url = sitelink.get('url')
                        if wiki_url:
                            wiki_urls[key] = requests.utils.unquote(wiki_url)
                    return wiki_urls
    return None


def page_open_body(name):
    resp = req.get(name)
    soup = BeautifulSoup(resp.text, 'lxml')
    main_part = str(soup.body)
    return main_part


# ФУНКЦИЯ ПОЛУЧЕНИЯ ДАТЫ НАЧАЛО
def get_dates_from_url(url, name):
    def get_dates(page, pattern):
        new = re.findall(pattern, str(page))

        date = ''
        date_list = []
        state = False
        for j in new:
            for i in j:
                if i == '<':
                    state = True
                if i == '>':
                    state = False
                if i == '<':
                    state = True
                if i == '>':
                    state = False
                if i == '[':
                    state = True
                if i == ']':
                    state = False
                if not state:
                    if i != ']' and i != '>':
                        date += i
                        temp = i
            date_list.append(date)
            date = ''

        data_list_new = []

        for i in date_list:
            new_elem = i.replace(u'\xa0', u' ')
            data_list_new.append(new_elem)

        return data_list_new

    changer = page_open_body(url)

    soup = BeautifulSoup(changer)
    page = soup.find('table', {'class': 'infobox vcard'})

    data_pattern = re.compile(r'%s</a>.*?office(.*?)</tr><tr>' % name)

    data_list = get_dates(page, data_pattern)

    if not data_list:
        data_pattern = re.compile(r'%s</a>.*?eign(.*?)</tr><tr>' % name)
        data_list = get_dates(page, data_pattern)

    return data_list


# ФУНКЦИЯ ПОЛУЧЕНИЯ ДАТЫ КОНЕЦ

wd_url = []

main_elem = page_open_body("https://en.wikipedia.org/wiki/List_of_state_leaders_in_1900")
pattern = re.compile(r'href="/wiki/(.*?)"')
searcher = re.findall(pattern, main_elem)

new_searcher = []
for i in searcher:
    match = re.search(r'[\.:]', i)
    if not match:
        new_searcher.append(i)

href_list = new_searcher
print(len(href_list))
n = 0
for j in href_list:
    n += 1
    try:
        new_url = "https://en.wikipedia.org/wiki/" + j
        main_elem = page_open_body(new_url)

        pattern = re.compile(r'www\.wikidata\.org/wiki/Special:EntityPage/(.*?)"')
        searcher = re.findall(pattern, main_elem)
        wd_url.append(searcher[0])
        print('страница %s закрыта' % n)
    except IndexError:
        None
        print('не вышло..')
print(wd_url)  # СПИСОК ССЫЛОК В ФОРМАТЕ Q*****

'''
headers_dict = {}
names = []
for i in wd_url:
    try:
        sparql = SPARQLWrapper("http://query.wikidata.org/sparql", agent=UserAgent().random)
        sparql.setQuery("""
            SELECT ?inception WHERE {
              wd:%s wdt:P31 ?inception
            }
        """ % i)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        humanity = results['results']['bindings'][0]['inception']['value']

        if humanity == 'http://www.wikidata.org/entity/Q5':
            names.append(i)
            sparql = SPARQLWrapper("http://query.wikidata.org/sparql", agent=UserAgent().random)
            sparql.setQuery("""
                        SELECT ?inception WHERE {
                          wd:%s wdt:P1559 ?inception
                        }
                    """ % i)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            print(results['results']['bindings'][0]['inception']['value'])

            sparql = SPARQLWrapper("http://query.wikidata.org/sparql", agent=UserAgent().random)
            sparql.setQuery("""
                                        SELECT ?item ?itemLabel 
                                        WHERE 
                                        {
                                          wd:%s wdt:P39 ?item.
                                          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                                        }
                                    """ % i)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            print(results)
            headers_dict[i] = []
            for j in range(0, len(results['results']['bindings'])):
                main_elem = results['results']['bindings'][j]['item']['value']
                result = re.split('/', main_elem)[-1]
                headers_dict[i].append(result)

    except IndexError:
        None

print(headers_dict)
'''


def get_title(id):
    try:
        sparql = SPARQLWrapper("http://query.wikidata.org/sparql", agent=UserAgent().random)
        sparql.setQuery("""
                                                                    SELECT ?item ?itemLabel 
                                                                    WHERE 
                                                                    {
                                                                      wd:%s wdt:P39 ?item.
                                                                      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                                                                    }
                                                                """ % id)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results
    except:
        return None


def get_subclass(id):
    try:
        sparql = SPARQLWrapper("http://query.wikidata.org/sparql", agent=UserAgent().random)
        sparql.setQuery("""
                                                                        SELECT ?item ?itemLabel 
                                                                        WHERE 
                                                                        {
                                                                          wd:%s wdt:P279 ?item.
                                                                          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                                                                        }
                                                                    """ % id)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results
    except:
        return


def ruller_cheeck(position_name):
    header_pattern = re.compile(r'head|ruler')
    match = re.match(header_pattern, position_name)
    if match:
        return True
    return False


not_needed_positions = {}
needed_positions = {}


def get_position(id, step=0, name=False):
    global checked_positions
    if step == 0:
        positions_held = get_title(id)
        if positions_held == None:
            return None
        for i in positions_held['results']['bindings']:
            current_position_link = i['item']['value']
            current_position_id = re.split('/', current_position_link)[-1]
            current_position_name = i['itemLabel']['value']
            if needed_positions.get(current_position_id) or ruller_cheeck(current_position_name):
                needed_positions[current_position_id] = True
                if name == False:
                    return current_position_id
                else:
                    return current_position_name
            if not_needed_positions.get(current_position_id):
                return
            current_position_subclass_id = get_position(current_position_id, step + 1)
            if needed_positions.get(current_position_id) or current_position_subclass_id != None:
                needed_positions[current_position_id] = True
                checked_positions = {}
                if name == False:
                    return current_position_id
                else:
                    return current_position_name
            not_needed_positions[current_position_id] = True
        return
    else:
        positions_held = get_subclass(id)
        if positions_held == None:
            return
        for i in positions_held['results']['bindings']:
            current_position_link = i['item']['value']
            current_position_id = re.split('/', current_position_link)[-1]
            current_position_name = i['itemLabel']['value']
            if needed_positions.get(current_position_id) or ruller_cheeck(current_position_name):
                needed_positions[current_position_id] = True
                if name == False:
                    return current_position_id
                else:
                    return current_position_name
            if not_needed_positions.get(current_position_id):
                return
            current_position_subclass_id = get_position(current_position_id, step + 1)
            if needed_positions.get(current_position_id) or current_position_subclass_id != None:
                needed_positions[current_position_id] = True
                if name == False:
                    return current_position_id
                else:
                    return current_position_name
            not_needed_positions[current_position_id] = True
        return


head_dict = {}
for i in searcher:
    print(get_position(i))
    if get_position(i) is not None:
        head_dict[i] = []
        head_dict[i].append(get_position(i))
        head_dict[i].append(get_position(i, name=True))

headers_dict = {}
for i in headers_dict:
    url = get_wiki_url(i)
    ans = get_dates_from_url(url)

print(ans)
