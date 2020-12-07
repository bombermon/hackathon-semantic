data = {'Q40787': ['Q11696', 'Emperor of All Russia'], 'Q7747': ['Q60497063', 'President of Russia'],
        'Q7996': ['Q11696', 'Tsar of Russia'], 'Q22686': ['Q11696', 'President of the United States']}
import re
from bs4 import BeautifulSoup
import requests as req
import datefinder

def page_open_body(name):
    resp = req.get(name)
    soup = BeautifulSoup(resp.text, 'lxml')
    main_part = str(soup.body)
    return main_part



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

    changer = page_open_body(url)

    soup = BeautifulSoup(changer)
    page = soup.find('table', {'class': 'infobox vcard'})

    data_pattern = re.compile(r'%s</a>.*?office(.*?)</tr><tr>' % name)
    data_list = get_dates(page, data_pattern)

    if not data_list:
        data_pattern = re.compile(r'%s</a>.*?eign(.*?)</tr><tr>' % name)
        data_list = get_dates(page, data_pattern)

    temp_str = data_list[0]
    temp_str = re.sub(r"[#%!@*,.;]", "", temp_str)
    data_list = re.split('–', temp_str)
    new_data = []
    for k in data_list:
        k = k.replace(' ', '')

        if k.isdigit() == False:
            matches = datefinder.find_dates(k)
            for match in matches:
                new_str = str(match)
                new_str = re.split(' ', new_str)
                new_str[0] = new_str[0].replace('-', '.')
                temper_list = new_str[0].split('.')
                print(temper_list)
                new_str[0] = temper_list[2] + '.' + temper_list[1] + '.' + temper_list[0]



                new_data.append(new_str[0])
        if k.isdigit():
            new_data.append(k)

    if len(new_data) == 1:
        new_data.append('по наст. время')
    if str(new_data[0]).isdigit():
        new_data[0] = '1.01.' + new_data[0]
        new_data.append('2') # СТАВИМ ВТОРОЙ УРОВЕНЬ

    else:
        new_data.append('0')


    if new_data[1].isdigit():
        new_data[1] = '1.01.' + new_data[1]
        new_data.append('2')  # СТАВИМ ПЕРВЫЙ УРОВЕНЬ
    else:
        new_data.append('0')



    return new_data

new_list = []
for i in data:
    url = get_wiki_url(i)
    ans = get_dates_from_url(url, data[i][1])
    data[i].append(ans[0])
    data[i].append(ans[1])
    data[i].append(ans[2])
    data[i].append(ans[3])

print(data)

