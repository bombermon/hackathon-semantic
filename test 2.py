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
            if i == '(':
                state = True
            if i == ')':
                state = False

            if not state:
                if i != ']' and i != '>' and i != ')':
                    date += i
        date_list.append(date)
        date = ''

    data_list_new = []

    for i in date_list:
        new_elem = i.replace(u'\xa0', u' ')
        data_list_new.append(new_elem)

    return data_list_new


title = 'king'

url = 'https://en.wikipedia.org/wiki/Seleucus_VII_Philometor'
changer = page_open_body(url)

soup = BeautifulSoup(changer)
page = soup.find('table', {'class': 'infobox vcard'})

data_pattern = re.compile(r'%s</a>.*?office(.*?)</tr><tr>' % title)
data_list = get_dates(page, data_pattern)

if not data_list:
    data_pattern = re.compile(r'%s</a>.*?eign(.*?)</tr><tr>' % title)
    data_list = get_dates(page, data_pattern)
    if not data_list:
        data_pattern = re.compile(r'eign(.*?)</tr><tr>')
        data_list = get_dates(page, data_pattern)
is_BC = False
temp_str = data_list[0]

pattern = re.compile(r'BC')
match = re.findall(pattern, temp_str)
if match:
    temp_str = temp_str.replace('BC', '')
    is_BC = True
pattern = re.compile(r'BCE')
match = re.findall(pattern, temp_str)
if match:
    temp_str = temp_str.replace('BCE', '')
    is_BC = True
pattern = re.compile(r'AC')
match = re.findall(pattern, temp_str)
if match:
    temp_str = temp_str.replace('AC', '')
    is_BC = True
pattern = re.compile(r'AD')
match = re.findall(pattern, temp_str)
if match:
    temp_str = temp_str.replace('AD', '')
if is_BC:
    pattern = re.compile(r'c\.')
    match = re.findall(pattern, temp_str)
    if match:
        temp_str = temp_str.replace('c.', '')



temp_str = re.sub(r"[#%!@*,.;]", "", temp_str)
data_list = re.split('–', temp_str)
new_data = [-1, -1, -1, -1]
n = 0
for k in data_list:
    k = k.replace(' ', '')
    if n > 3:
        break
    if k.isdigit() == False:
        matches = datefinder.find_dates(k)
        for match in matches:
            new_str = str(match)
            new_str = re.split(' ', new_str)
            new_str[0] = new_str[0].replace('-', '.')
            temper_list = new_str[0].split('.')

            new_str[0] = temper_list[2] + '.' + temper_list[1] + '.' + temper_list[0]
            new_data[n] = new_str[0]
    if k.isdigit():
        new_data[n] = k
    n += 2

if str(new_data[0]).isdigit():
    if is_BC:
        new_data[0] = '-1.01.' + new_data[0]
    else:
        new_data[0] = '1.01.' + new_data[0]
    new_data[1] = '2'
else:
    new_data[1] = '0'

if new_data[2] == -1:
    new_data[2] = 'по наст. время'
    new_data[3] = '0'

if new_data[2].isdigit():
    if is_BC:
        new_data[2] = '-1.01.' + new_data[2]
    else:
        new_data[2] = '1.01.' + new_data[2]
    new_data[3] = '2'  # СТАВИМ ПЕРВЫЙ УРОВЕНЬ
else:
    new_data[3] = '0'
print(new_data)
for count in new_data:
    if count == -1:
        new_data = None
if new_data != None:
    temp = new_data
    new_data = []
    new_data.append(temp)
print(new_data)
