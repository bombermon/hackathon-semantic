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


main_elem = page_open_body("https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States")
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





'''
sparql = SPARQLWrapper("http://query.wikidata.org/sparql", agent=UserAgent().random)
sparql.setQuery("""
    {
    "batchcomplete": "",
    "query": {
        "normalized": [
            {
                "from": "%s",
                "to": "%s"
            }
        ],
        "pages": {
            "-1": {
                "ns": 0,
                "title": "%s",
                "missing": ""
            }
        }
    }
}
""" % 'Federal_government_of_the_United_States')
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print(results)
'''