from bs4 import BeautifulSoup
import requests as req
import re
from SPARQLWrapper import SPARQLWrapper, JSON
from fake_useragent import UserAgent
import wikipedia


resp = req.get("https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States")





soup = BeautifulSoup(resp.text, 'lxml')
main_elem = str(soup.tbody)


pattern = re.compile(r'href="/wiki/(.*?)"')
searcher = re.findall(pattern, main_elem)
for i in searcher:
    match = re.search(r'[.]', i)
    if match:
        searcher.remove(i)
print(searcher)

new_url = "https://en.wikipedia.org/wiki/" + searcher[0]
print(new_url)
#print(soup.tbody)



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