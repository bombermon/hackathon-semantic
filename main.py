from bs4 import BeautifulSoup
import requests as req
import re
from SPARQLWrapper import SPARQLWrapper, JSON
from fake_useragent import UserAgent
import wikipedia

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

main_elem = page_open_tbody("https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States")

pattern = re.compile(r'href="/wiki/(.*?)"')
searcher = re.findall(pattern, main_elem)
for i in searcher:
    match = re.search(r'[.]', i)
    if match:
        searcher.remove(i)
print(searcher)

new_url = "https://en.wikipedia.org/wiki/" + searcher[0]


main_elem = page_open_body(new_url)

pattern = re.compile(r'www\.wikidata\.org/wiki/Special:EntityPage/(.*?)"')
searcher = re.findall(pattern, main_elem)
for i in searcher:
    match = re.search(r'[.]', i)
    if match:
        searcher.remove(i)

wd_url = searcher[0]
print(wd_url)


#print(soup.tbody)


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