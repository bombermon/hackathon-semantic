from bs4 import BeautifulSoup
import requests as req
import re

import datefinder

def page_open_body(name):
    resp = req.get(name)
    soup = BeautifulSoup(resp.text, 'lxml')
    main_elem = str(soup.body)
    return main_elem

wd_url = []


main_elem = page_open_body("https://en.wikipedia.org/wiki/Nicholas_II_of_Russia")

# Beautiful Soup
soup = BeautifulSoup(main_elem)
film_list = soup.find('table', {'class': 'infobox vcard'})
#pattern = re.compile(r'eign</th><td>(.*?)</td>')

pattern = re.compile(r'<tr>(.*?)eign(.*?)</tr><tr>')
new = re.findall(pattern, str(film_list))



print(new)

date = ''
date_list = []
state = False
for j in new[0]:
    for i in j:
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
    date_list.append(date)
    date = ''
print(date_list)