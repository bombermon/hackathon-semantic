import re

searcher = ['Q48352', 'Q2285706', 'Q30', 'Q877353', 'Q524572',
            'Q47586', 'Q35798', 'Q48525', 'Q380782', 'Q11211', 'Q23', 'Q35171', 'Q22686', 'Q27809653', 'Q6279',
            'Q97738250', 'Q6659249', 'Q11869', 'Q214679', 'Q11896', 'Q1829415', 'Q91', 'Q35041', 'Q9588', 'Q20711778',
            'Q11881', 'Q3112663', 'Q217797', 'Q25046283', 'Q9582', 'Q203433']
from SPARQLWrapper import SPARQLWrapper, JSON
from fake_useragent import UserAgent


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
    header_pattern = re.compile(r'head|ruler')
    match = re.match(header_pattern, position_name)
    if match:
        return True
    return False

not_needed_positions = {}
needed_positions = {}

def get_position(id ,step = 0):
    global checked_positions
    if step == 0:
        positions_held = get_title(id)
        if positions_held == None:
            return None
        for i in positions_held['results']['bindings']:
            current_position_link = i['item']['value']
            current_position_id = re.split('/', current_position_link)[-1]
            current_position_name = i['itemLabel']['value']
            if needed_positions.get(current_position_id) or ruller_cheeck(current_position_name):
                needed_positions[current_position_id] = True
                return current_position_id
            if not_needed_positions.get(current_position_id):
                return
            current_position_subclass_id = get_position(current_position_id, step + 1)
            if needed_positions.get(current_position_id) or current_position_subclass_id != None:
                needed_positions[current_position_id] = True
                checked_positions = {}
                return current_position_id
            not_needed_positions[current_position_id] = True
        return
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
            current_position_subclass_id = get_position(current_position_id, step + 1)
            if needed_positions.get(current_position_id) or current_position_subclass_id != None:
                needed_positions[current_position_id] = True
                return current_position_id
            not_needed_positions[current_position_id] = True
        return
head_dict = {}
for i in searcher:
    print(get_position(i))
    if get_position(i) is not None:
        head_dict[i] = []
        head_dict[i].append(get_position(i))

print(head_dict)