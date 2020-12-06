from bs4 import BeautifulSoup
import requests as req
import re
from SPARQLWrapper import SPARQLWrapper, JSON
from fake_useragent import UserAgent
import wikipedia

'''
Берем значит ссылку и через семантик веб анализируем человек это или не человек имя это или не имя 
'''

def page_open_tbody(name):
    resp = req.get(name)
    soup = BeautifulSoup(resp.text, 'lxml')
    main_elem = str(soup.tbody)
    return main_elem

def page_open_body(name):
    resp = req.get(name)
    soup = BeautifulSoup(resp.text, 'lxml')
    main_elem = str(soup.body)
    return main_elem

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
        print('не вышло..')
print(wd_url)


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
            print('УРА МЕШОК С КОСТЯМИ КОЖАНЫЙ %s' % i)
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
        else:
            print('ЭТО НЕ ХУЙНЯ НО И НЕ МЕШОК %s' % i)

    except IndexError:
        print('Это хуйня ' + i)




print(headers_dict)




