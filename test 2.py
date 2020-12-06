from bs4 import BeautifulSoup
import requests as req
import re

import datefinder

def get_dates_from_url(url):
    def page_open_body(name):
        resp = req.get(name)
        soup = BeautifulSoup(resp.text, 'lxml')
        main_elem = str(soup.body)
        return main_elem

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


    wd_url = []



    main_elem = page_open_body(url)

    soup = BeautifulSoup(main_elem)
    page = soup.find('table', {'class': 'infobox vcard'})


    pattern = re.compile(r'<tr>.*?office(.*?)</tr><tr>')

    data_list = get_dates(page, pattern)


    if not data_list:
        pattern = re.compile(r'<tr>.*?eign(.*?)</tr><tr>')
        data_list = get_dates(page, pattern)

    return data_list