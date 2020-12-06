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

main_elem = page_open_body("https://en.wikipedia.org/wiki/Thomas_Jefferson")

# Beautiful Soup
soup = BeautifulSoup(main_elem)
film_list = soup.find('table', {'class': 'infobox vcard'})
# pattern = re.compile(r'eign</th><td>(.*?)</td>')

# pattern = re.compile(r'<tr>.*?eign(.*?)</tr><tr>')
pattern = re.compile(r'<tr>.*?office(.*?)</tr><tr>')
new = re.findall(pattern, str(film_list))

print(new)

date = ''
date_list = []
state = False
for j in new:
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
                temp = i
    date_list.append(date)
    date = ''
'''
data_list_new = []
new_str = ''
flag = False
for i in date_list:
    for j in i:
        if not flag:
            if j.isdigit():
                temp_type = 'digit'
            if j.isalpha():
                temp_type = 'word'
            temp = j
            flag = True
        if j.isdigit():
            current_type = 'digit'
        if j.isalpha():
            current_type = 'word'
        if current_type == temp_type:
            new_str += j
        if j.isdigit():
            temp_type = 'digit'
        if j.isalpha():
            temp_type = 'word'
print(new_str)

'''

print(date_list)
