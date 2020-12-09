from bs4 import BeautifulSoup
import requests as req
import re
from SPARQLWrapper import SPARQLWrapper, JSON
from fake_useragent import UserAgent
import csv
import datefinder
'''
Берем значит ссылку и через семантик веб анализируем человек это или не человек имя это или не имя 
'''

def save_data(file_name, data):

    table_rows = []
    temp_row = {"person": '', "position": '', "start_precision": '', "start": '', "end_precision": '', "end": ''}
    for i in data.keys():
        try:
            current_row = temp_row
            current_row["person"] = "https://www.wikidata.org/wiki/" + i
            current_row["position"] = "https://www.wikidata.org/wiki/" + data[i][0]
            current_row["start_precision"] = data[i][4]
            current_row["start"] = data[i][2]
            current_row["end_precision"] = data[i][5]
            current_row["end"] = data[i][3]
            table_rows.append(current_row.copy())
        except:
            None
    with open(file_name + '.csv', 'w', encoding='UTF-8') as csv_file:  # ОТКРЫВАЕМ (ИЛИ СОЗДАЕМ ФАЙЛ CSV НА ЗАПИСЬ СЛОВАРЯ)
        writer = csv.DictWriter(csv_file, fieldnames = temp_row.keys())
        writer.writeheader()
        writer.writerows(table_rows)

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



# ФУНКЦИЯ ПОЛУЧЕНИЯ ДАТЫ КОНЕЦ
wd_url = []


main_elem = page_open_body("https://en.wikipedia.org/wiki/List_of_state_leaders_in_%s" % 1999)
print(main_elem)
pattern = re.compile(r'href="/wiki/(.*?)"')
searcher = re.findall(pattern, main_elem)

new_searcher = []
for i in searcher:
    match = re.search(r'[\.:]', i)
    if not match:
        new_searcher.append(i)

href_list = new_searcher
print(href_list)
n = 0
for j in href_list:
    try:
        new_url = "https://en.wikipedia.org/wiki/" + j
        main_elem = page_open_body(new_url)
        pattern = re.compile(r'www\.wikidata\.org/wiki/Special:EntityPage/(.*?)"')
        searcher = re.findall(pattern, main_elem)
        print(searcher)
        sparql = SPARQLWrapper("http://query.wikidata.org/sparql", agent=UserAgent().random)
        sparql.setQuery("""
                   SELECT ?inception WHERE {
                     wd:%s wdt:P31 ?inception
                   }
               """ % searcher[0])
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print(results)
        humanity = results['results']['bindings'][0]['inception']['value']
        print(humanity)

        if humanity == 'http://www.wikidata.org/entity/Q5':
            wd_url.append(searcher[0])
            n += 1
            print('страница %s закрыта ' % n, j)
            print(wd_url)
    except IndexError:
        None
        print('не вышло..')
print(wd_url)  # СПИСОК ССЫЛОК В ФОРМАТЕ Q*****
