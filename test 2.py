from bs4 import BeautifulSoup
import requests as req
import re
from SPARQLWrapper import SPARQLWrapper, JSON
from fake_useragent import UserAgent
import csv
import datefinder

wd_url = ["Q57920"]

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
            return None
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
                return
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


head_dict = {}
for i in wd_url:
    positions_id_list, positions_name_list = get_positions_id_and_name_list(i)
    print(positions_name_list)
    if positions_id_list is not None:
        head_dict[i] = []
        head_dict[i].append(positions_id_list)
        head_dict[i].append(positions_name_list)

print(head_dict)