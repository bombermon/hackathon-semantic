
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


# ФУНКЦИЯ ПОЛУЧЕНИЯ ДАТЫ НАЧАЛО
def get_dates_from_url(url, name, title):
    try:
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

        sparql = SPARQLWrapper("http://query.wikidata.org/sparql", agent=UserAgent().random)
        sparql.setQuery("""SELECT ?Title ?starttimeValue ?TitleLabel ?starttimePrecision ?endtimeValue ?endtimePrecision  WHERE {
    wd:%s p:P39 ?TitleStatementNode.
    ?TitleStatementNode ps:P39 ?Title.
    ?TitleStatementNode pqv:P580 ?starttimenode.
    ?TitleStatementNode pqv:P582 ?endtimenode.
    ?starttimenode wikibase:timeValue         ?starttimeValue.
    ?starttimenode wikibase:timePrecision     ?starttimePrecision.
    ?endtimenode wikibase:timeValue         ?endtimeValue.
    ?endtimenode wikibase:timePrecision     ?endtimePrecision.
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }


    }""" % name)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        title_dict = {}
        counter_dict = {}
        for i in range(0, len(results['results']['bindings'])):
            state_repeat = False

            Title_ID = results['results']['bindings'][i]['TitleLabel']['value']
            Title_ID = re.split('/', Title_ID)[-1]
            if Title_ID == title:
                if Title_ID in title_dict:
                    state_repeat = True
                    counter_dict[Title_ID] = counter_dict[Title_ID] + 1
                    title_dict[Title_ID].append([-1, -1, -1, -1])
                else:
                    counter_dict[Title_ID] = 1
                    title_dict[Title_ID] = []
                    title_dict[Title_ID].append([-1, -1, -1, -1])
                if state_repeat:
                    number = counter_dict[Title_ID] - 1

                    start_pos = results['results']['bindings'][i]['starttimeValue']['value']
                    start_pos = re.split('T', start_pos)[0]

                    BC_state = False
                    if start_pos[0] == '-':
                        BC_state = True
                        start_pos[1:]

                    state_to_write = False
                    new_word = ''
                    for char in start_pos:
                        if char != '0':
                            state_to_write = True
                        if state_to_write:
                            new_word += char
                    start_pos = new_word

                    start_pos = start_pos.replace('-', '.')
                    start_pos = list(reversed(start_pos.split('.')))
                    start_pos = '.'.join(start_pos)

                    if BC_state:
                        title_dict[Title_ID][number][0] = '-' + start_pos
                    else:
                        title_dict[Title_ID][number][0] = start_pos

                    start_accuracy = results['results']['bindings'][i]['starttimePrecision']['value']
                    title_dict[Title_ID][number][1] = str(11 - int(start_accuracy))

                    end_pos = results['results']['bindings'][i]['endtimeValue']['value']
                    end_pos = re.split('T', end_pos)[0]

                    if end_pos[0] == '-':
                        BC_state = True
                        end_pos[1:]

                    state_to_write = False
                    new_word = ''
                    for char in end_pos:
                        if char != '0':
                            state_to_write = True
                        if state_to_write:
                            new_word += char
                    end_pos = new_word

                    end_pos = end_pos.replace('-', '.')
                    end_pos = list(reversed(end_pos.split('.')))
                    end_pos = '.'.join(end_pos)

                    if BC_state:
                        title_dict[Title_ID][number][2] = '-' + end_pos
                    else:
                        title_dict[Title_ID][number][2] = end_pos

                    end_accuracy = results['results']['bindings'][i]['endtimePrecision']['value']
                    title_dict[Title_ID][number][3] = str(11 - int(end_accuracy))
                else:
                    start_pos = results['results']['bindings'][i]['starttimeValue']['value']
                    start_pos = re.split('T', start_pos)[0]

                    BC_state = False
                    if start_pos[0] == '-':
                        BC_state = True
                        start_pos[1:]

                    state_to_write = False
                    new_word = ''
                    for char in start_pos:
                        if char != '0':
                            state_to_write = True
                        if state_to_write:
                            new_word += char
                    start_pos = new_word

                    start_pos = start_pos.replace('-', '.')
                    start_pos = list(reversed(start_pos.split('.')))
                    start_pos = '.'.join(start_pos)
                    if BC_state:
                        title_dict[Title_ID][0][0] = '-' + start_pos
                    else:
                        title_dict[Title_ID][0][0] = start_pos

                    start_accuracy = results['results']['bindings'][i]['starttimePrecision']['value']
                    title_dict[Title_ID][0][1] = str(11 - int(start_accuracy))

                    end_pos = results['results']['bindings'][i]['endtimeValue']['value']
                    end_pos = re.split('T', end_pos)[0]

                    if end_pos[0] == '-':
                        BC_state = True
                        end_pos[1:]

                    state_to_write = False
                    new_word = ''
                    for char in end_pos:
                        if char != '0':
                            state_to_write = True
                        if state_to_write:
                            new_word += char
                    end_pos = new_word

                    end_pos = end_pos.replace('-', '.')
                    end_pos = list(reversed(end_pos.split('.')))
                    end_pos = '.'.join(end_pos)

                    if BC_state:
                        title_dict[Title_ID][0][2] = '-' + end_pos
                    else:
                        title_dict[Title_ID][0][2] = end_pos

                    end_accuracy = results['results']['bindings'][i]['endtimePrecision']['value']
                    title_dict[Title_ID][0][3] = str(11 - int(end_accuracy))



        # ПОЛУЧЕНИЕ ЗАПРОСА ДОЛЖНОСТЕЙ КОТОРЫЕ СЕЙЧАС ПРАВЯТ

        sparql = SPARQLWrapper("http://query.wikidata.org/sparql", agent=UserAgent().random)
        sparql.setQuery("""SELECT ?Title ?starttimeValue ?starttimePrecision ?TitleLabel ?endtimeValue ?endtimePrecision  WHERE {
          wd:%s p:P39 ?TitleStatementNode.
          ?TitleStatementNode ps:P39 ?Title.
          ?TitleStatementNode pqv:P580 ?starttimenode.
          ?starttimenode wikibase:timeValue         ?starttimeValue.
          ?starttimenode wikibase:timePrecision     ?starttimePrecision.
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }


        }""" % name)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        first_got = False
        for i in range(0, len(results['results']['bindings'])):
            if first_got:
                break
            Title_ID = results['results']['bindings'][i]['TitleLabel']['value']
            Title_ID = re.split('/', Title_ID)[-1]
            start_pos = results['results']['bindings'][i]['starttimeValue']['value']
            start_pos = re.split('T', start_pos)[0]

            BC_state = False
            if start_pos[0] == '-':
                BC_state = True
                start_pos[1:]
            state_to_write = False
            new_word = ''
            for char in start_pos:
                if char != '0':
                    state_to_write = True
                if state_to_write:
                    new_word += char
            start_pos = new_word

            start_pos = start_pos.replace('-', '.')
            start_pos = list(reversed(start_pos.split('.')))
            start_pos = '.'.join(start_pos)

            if Title_ID in title_dict and not BC_state:
                for j in range(0, len(title_dict[Title_ID])):

                    if start_pos != title_dict[Title_ID][j][0]:

                        title_dict[Title_ID].append([-1, -1, -1, -1])
                        if BC_state:
                            title_dict[Title_ID][-1][0] = '-' + start_pos
                        else:
                            title_dict[Title_ID][-1][0] = start_pos
                        start_accuracy = results['results']['bindings'][i]['starttimePrecision']['value']
                        title_dict[Title_ID][-1][1] = str(11 - int(start_accuracy))
                        title_dict[Title_ID][-1][2] = 'по наст. время'
                        title_dict[Title_ID][-1][3] = '0'
                        first_got = True
                        break

        if title_dict != {}:
            new_data = title_dict[title]
        if title_dict == {}:
            print('Вход совершен')
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

            temp_str = data_list[0]
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
                new_data[0] = '1.01.' + new_data[0]
                new_data[1] = '2'
            else:
                new_data[1] = '0'

            if new_data[2] == -1:
                new_data[2] = 'по наст. время'
                new_data[3] = '0'

            if new_data[2].isdigit():
                new_data[2] = '1.01.' + new_data[2]
                new_data[3] = '2'  # СТАВИМ ПЕРВЫЙ УРОВЕНЬ
            else:
                new_data[3] = '0'

            temp = new_data
            new_data = []
            new_data.append(temp)
        return new_data
    except:
        None




def get_title(id):
    try:
        sparql = SPARQLWrapper("http://query.wikidata.org/sparql", agent=UserAgent().random)
        sparql.setQuery("""
                                                                    SELECT ?item ?itemLabel 
                                                                    WHERE 
                                                                    {
                                                                      wd:%s wdt:P39 ?item.
                                                                      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                                                                    }
                                                                """ % id)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results
    except:
        return None



def get_subclass(id):
    try:
        sparql = SPARQLWrapper("http://query.wikidata.org/sparql", agent=UserAgent().random)
        sparql.setQuery("""
                                                                        SELECT ?item ?itemLabel 
                                                                        WHERE 
                                                                        {
                                                                          wd:%s wdt:P279 ?item.
                                                                          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                                                                        }
                                                                    """ % id)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results
    except:
        return


def ruller_cheeck(position_name):
    header_pattern = re.compile(r'head of state|ruler')
    match = re.match(header_pattern, position_name)
    if match:
        return True
    return False

not_needed_positions = {}
needed_positions = {}

def get_positions_id_and_name_list(id, step=0):
    if step == 0:
        ruler_positions_id_list = []
        ruler_positions_name_list = []
        positions_held = get_title(id)
        if positions_held == None:
            return None, None
        for i in positions_held['results']['bindings']:
            current_position_link = i['item']['value']
            current_position_id = re.split('/', current_position_link)[-1]
            current_position_name = i['itemLabel']['value']
            if needed_positions.get(current_position_id) or ruller_cheeck(current_position_name):
                needed_positions[current_position_id] = True
                ruler_positions_id_list.append(current_position_id)
                ruler_positions_name_list.append(current_position_name)
                continue
            if not_needed_positions.get(current_position_id):
                continue
            current_position_subclass_id = get_positions_id_and_name_list(current_position_id, step + 1)
            if needed_positions.get(current_position_id) or current_position_subclass_id != None:
                needed_positions[current_position_id] = True
                ruler_positions_id_list.append(current_position_id)
                ruler_positions_name_list.append(current_position_name)
                continue
            not_needed_positions[current_position_id] = True
        if len(ruler_positions_id_list) == 0:
            return None, None
        else:
            return ruler_positions_id_list, ruler_positions_name_list
    else:
        positions_held = get_subclass(id)
        if positions_held == None:
            return
        for i in positions_held['results']['bindings']:
            current_position_link = i['item']['value']
            current_position_id = re.split('/', current_position_link)[-1]
            current_position_name = i['itemLabel']['value']
            if needed_positions.get(current_position_id) or ruller_cheeck(current_position_name):
                needed_positions[current_position_id] = True
                return current_position_id
            if not_needed_positions.get(current_position_id):
                return
            current_position_subclass_id = get_positions_id_and_name_list(current_position_id, step + 1)
            if needed_positions.get(current_position_id) or current_position_subclass_id != None:
                needed_positions[current_position_id] = True
                return current_position_id
            not_needed_positions[current_position_id] = True
        return None


head_dict = {'Q7747': [['Q10962705'], ['President of Russia']], 'Q515704': [['Q27330121'], ['King of Thailand']], 'Q10061': [['Q268218'], ['Emperor of China']], 'Q349440': [['Q208233'], ['Emperor of Japan']], 'Q484359': [['Q22304810'], ['King of Joseon Dynasty']], 'Q8597': [['Q15390704'], ['Mughal emperor']], 'Q907317': [['Q56230659'], ['King of Ryukyu']], 'Q153586': [['Q1294765', 'Q18341329'], ['monarch of Norway', 'monarch of Denmark']], 'Q7207': [['Q12097', 'Q18810062'], ['king', 'monarch of England']], 'Q936976': [['Q3439798', 'Q29166132'], ['King of France and Navarre', 'king of Navarre']], 'Q150586': [['Q12097', 'Q181765'], ['king', 'Holy Roman Emperor']], 'Q57206': [['Q19827831', 'Q23011565'], ['Count Palatine of the Rhine', 'duke of Bavaria']], 'Q70705': [['Q20860025'], ['Prince-Archbishop']], 'Q62160': [['Q63375991', 'Q63871039'], ['Duke of Schleswig', 'Duke of Holstein']], 'Q452580': [['Q95688080'], ['Duke of Montferri']], 'Q544873': [['Q477406'], ['regent']], 'Q34464': [['Q835706', 'Q1542521', 'Q3847454', 'Q58631963', 'Q58637583', 'Q58800860'], ['Prince of Asturias', 'Governor-General of the Philippines', 'King of Spain', 'monarch of Aragon', 'monarch of Spain', 'Monarch of Portugal']], 'Q171465': [['Q15315411'], ['sultan of the Ottoman Empire']], 'Q52940': [['Q1268572', 'Q3273712'], ['monarch of Sweden', 'king of Poland']], 'Q170172': [['Q44356'], ['tsar']], 'Q79972': [['Q18810062', 'Q18810063', 'Q18810066'], ['monarch of England', 'monarch of Scotland', 'Monarch of Ireland']], 'Q52939': [['Q1268572'], ['monarch of Sweden']], 'Q164062': [['Q549449', 'Q66096255'], ['Prince of Orange', 'stadtholder of Holland']], 'Q171349': [['Q184299'], ['Shah']]}



new_list = []
table_rows = []
temp_row = {"person": '', "position": '', "start_precision": '', "start": '', "end_precision": '', "end": ''}
for i in head_dict:
    new_dict = {}
    ans = {}
    temp_dict = head_dict[i][1]

    for j in temp_dict:
        url = get_wiki_url(i)
        ans[temp_dict.index(j)] = get_dates_from_url(url, i, j)
    for k in range(0, len(temp_dict)):
        new_dict[head_dict[i][0][k]] = ans[k]
        current_row = temp_row
        current_row["person"] = "https://www.wikidata.org/wiki/" + i
        current_row["position"] = "https://www.wikidata.org/wiki/" + head_dict[i][0][k]
        for l in ans[k]:
            current_row["start_precision"] = l[1]
            current_row["start"] = l[0]
            current_row["end_precision"] = l[3]
            current_row["end"] = l[2]
            table_rows.append(current_row.copy())
    print(new_dict)

with open("Alt+F4_results" + '.csv', 'w', encoding='UTF-8') as csv_file:  # ОТКРЫВАЕМ (ИЛИ СОЗДАЕМ ФАЙЛ CSV НА ЗАПИСЬ СЛОВАРЯ)
    writer = csv.DictWriter(csv_file, fieldnames = temp_row.keys())
    writer.writeheader()
    writer.writerows(table_rows)
