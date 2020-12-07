import re

searcher = ['Q50199100', 'Q30', 'Q330963', 'Q48525', 'Q11698', 'Q692218', 'Q7689573', 'Q11268', 'Q11268', 'Q11701',
            'Q912994', 'Q170581', 'Q6508632', 'Q516515', 'Q6508632', 'Q766866', 'Q13751836', 'Q66096', 'Q11699',
            'Q24313', 'Q1140848', 'Q529294', 'Q1813203', 'Q355522', 'Q1813203', 'Q380900', 'Q48525', 'Q11696', 'Q22686',
            'Q11699', 'Q24313', 'Q639738', 'Q1066612', 'Q1355327', 'Q194907', 'Q11201', 'Q11147', 'Q11153', 'Q11142',
            'Q11124', 'Q11138', 'Q11107', 'Q11105', 'Q15488345', 'Q4962244', 'Q29863844', 'Q1641851', 'Q1614849',
            'Q6602759', 'Q5440562', 'Q279283', 'Q47566', 'Q1570656', 'Q7078911', 'Q669262', 'Q2916312', 'Q81665',
            'Q29552', 'Q29468', 'Q6579199', 'Q558334', 'Q849158', 'Q980036', 'Q7603694', 'Q11250358', 'Q3270264',
            'Q2747182', 'Q3308934', 'Q516156', 'Q7112705', 'Q11696', 'Q48352', 'Q2285706', 'Q30', 'Q877353', 'Q524572',
            'Q47586', 'Q35798', 'Q48525', 'Q380782', 'Q11211', 'Q23', 'Q35171', 'Q22686', 'Q27809653', 'Q6279',
            'Q97738250', 'Q6659249', 'Q11869', 'Q214679', 'Q11896', 'Q1829415', 'Q91', 'Q35041', 'Q9588', 'Q20711778',
            'Q11881', 'Q3112663', 'Q217797', 'Q25046283', 'Q9582', 'Q203433', 'Q25046275', 'Q11237', 'Q330963',
            'Q81665', 'Q162932', 'Q2824580', 'Q178903', 'Q11812', 'Q2824580', 'Q23', 'Q697949', 'Q11806', 'Q698073',
            'Q29092466', 'Q11806', 'Q42189', 'Q698093', 'Q11812', 'Q4206678', 'Q11812', 'Q42186', 'Q698106', 'Q179090',
            'Q698133', 'Q201646', 'Q29075153', 'Q11813', 'Q42186', 'Q698185', 'Q698407', 'Q219797', 'Q2824567',
            'Q11815', 'Q42186', 'Q564395', 'Q575757', 'Q2824558', 'Q11816', 'Q42186', 'Q618127', 'Q1541747',
            'Q20708389', 'Q11817', 'Q29552', 'Q698489', 'Q534192', 'Q11820', 'Q1720438', 'Q11820', 'Q29552', 'Q174492',
            'Q109463', 'Q11869', 'Q11869', 'Q42183', 'Q698694', 'Q11881', 'Q2824576', 'Q11881', 'Q42183', 'Q29552',
            'Q698731', 'Q11896', 'Q11896', 'Q42183', 'Q698769', 'Q12306', 'Q2824549', 'Q12306', 'Q42183', 'Q2824569',
            'Q12312', 'Q29552', 'Q698802', 'Q2824544', 'Q12325', 'Q29552', 'Q575819', 'Q7241091', 'Q91', 'Q29468',
            'Q698842', 'Q273546', 'Q80719', 'Q698908', 'Q8612', 'Q2824539', 'Q8612', 'Q80719', 'Q29552', 'Q29468',
            'Q698955', 'Q310852', 'Q698999', 'Q313302', 'Q29468', 'Q72251', 'Q29468', 'Q699120', 'Q29468', 'Q27333215',
            'Q35171', 'Q29552', 'Q699139', 'Q5665492', 'Q35678', 'Q29468', 'Q699168', 'Q27333215', 'Q35171', 'Q29552',
            'Q72472', 'Q310839', 'Q1720135', 'Q35041', 'Q29468', 'Q699201', 'Q310841', 'Q699227', 'Q33866', 'Q7241110',
            'Q33866', 'Q29468', 'Q699252', 'Q29092765', 'Q35648', 'Q29468', 'Q72835', 'Q2824579', 'Q34296', 'Q29552',
            'Q699289', 'Q699318', 'Q29468', 'Q699343', 'Q36023', 'Q29109910', 'Q36023', 'Q29468', 'Q699360',
            'Q29057270', 'Q35236', 'Q29468', 'Q699380', 'Q271023', 'Q29552', 'Q179868', 'Q298991', 'Q634429', 'Q699416',
            'Q596667', 'Q29552', 'Q568973', 'Q29468', 'Q699548', 'Q9588', 'Q699567', 'Q29552', 'Q699590', 'Q29552',
            'Q699646', 'Q209989', 'Q7241106', 'Q9588', 'Q29468', 'Q693742', 'Q203433', 'Q644161', 'Q9582', 'Q2824551',
            'Q9582', 'Q29468', 'Q11237', 'Q2824547', 'Q23685', 'Q29552', 'Q699693', 'Q49216', 'Q2824573', 'Q9960',
            'Q29468', 'Q699716', 'Q699744', 'Q29468', 'Q643015', 'Q49214', 'Q2824550', 'Q1124', 'Q29552', 'Q699776',
            'Q19673', 'Q659166', 'Q29468', 'Q327959', 'Q48259', 'Q464075', 'Q1379733', 'Q76', 'Q29552', 'Q45578',
            'Q6279', 'Q4226', 'Q27809653', 'Q22686', 'Q29468', 'Q699872', 'Q24313', 'Q101250908', 'Q97738250',
            'Q101369347', 'Q6279', 'Q29552', 'Q22923830', 'Q10853588', 'Q11816', 'Q1668757', 'Q8612', 'Q1851323',
            'Q35648', 'Q11147', 'Q6659249', 'Q2123628', 'Q186539', 'Q1857508', 'Q1030359', 'Q42189', 'Q42186', 'Q11817',
            'Q192852', 'Q1541747', 'Q3440208', 'Q7686034', 'Q48527', 'Q1025404', 'Q388602', 'Q7968411', 'Q80719',
            'Q2866985', 'Q217797', 'Q518155', 'Q494170', 'Q35525', 'Q131454', 'Q1640002', 'Q1472315', 'Q11696', 'Q23',
            'Q2824580', 'Q11806', 'Q29092466', 'Q11812', 'Q4206678', 'Q11813', 'Q29075153', 'Q11815', 'Q2824567',
            'Q11816', 'Q2824558', 'Q11817', 'Q20708389', 'Q11820', 'Q1720438', 'Q11869', 'Q11869', 'Q11881', 'Q2824576',
            'Q11896', 'Q11896', 'Q12306', 'Q2824549', 'Q12312', 'Q2824569', 'Q12325', 'Q2824544', 'Q91', 'Q7241091',
            'Q8612', 'Q2824539', 'Q35171', 'Q27333215', 'Q35678', 'Q5665492', 'Q35171', 'Q27333215', 'Q35041',
            'Q1720135', 'Q33866', 'Q7241110', 'Q35648', 'Q29092765', 'Q34296', 'Q2824579', 'Q36023', 'Q29109910',
            'Q35236', 'Q29057270', 'Q9588', 'Q7241106', 'Q9582', 'Q2824551', 'Q23685', 'Q2824547', 'Q9960', 'Q2824573',
            'Q1124', 'Q2824550', 'Q76', 'Q1379733', 'Q22686', 'Q27809653', 'Q6279', 'Q101250908', 'Q524901', 'Q11696',
            'Q11699', 'Q1030359', 'Q3099823', 'Q6606408', 'Q48769850', 'Q6274682', 'Q3243931', 'Q5277378', 'Q6659249',
            'Q6631599', 'Q3399518', 'Q6594922', 'Q220924', 'Q1829415', 'Q372565', 'Q5307593', 'Q60769168', 'Q263233',
            'Q6624341', 'Q6594913', 'Q1546583', 'Q6601903', 'Q6594915', 'Q17092531', 'Q16149281', 'Q6594910',
            'Q6602907', 'Q96372040', 'Q4793738', 'Q6594928', 'Q6594912', 'Q6594917', 'Q18148485', 'Q21335778',
            'Q6594911', 'Q4002712', 'Q6601898', 'Q6630669', 'Q2850068', 'Q7311321', 'Q185726', 'Q21068012', 'Q6603529',
            'Q48769850', 'Q16821820', 'Q6603528', 'Q6603531', 'Q60740651', 'Q6603530', 'Q97356206', 'Q6603532',
            'Q6643351', 'Q6603536', 'Q2123628', 'Q596135', 'Q1050554', 'Q47566', 'Q6602900', 'Q6602899', 'Q28406934',
            'Q24963437', 'Q28404720', 'Q19294', 'Q2738915', 'Q2248443', 'Q16203125', 'Q43401854', 'Q6601848',
            'Q65053271', 'Q65053290', 'Q19866629', 'Q6560662', 'Q6619393', 'Q6608756', 'Q55617489', 'Q1014848',
            'Q42897201', 'Q60518530', 'Q6626859', 'Q85778854', 'Q862444', 'Q1816883', 'Q280808', 'Q6609410', 'Q2108855',
            'Q6618068', 'Q6601897', 'Q97353920', 'Q7891356', 'Q6646996', 'Q3242839', 'Q7893164', 'Q11696', 'Q889821',
            'Q11250358', 'Q558677', 'Q575942', 'Q777288', 'Q777346', 'Q887010', 'Q842551', 'Q29514964', 'Q29514964',
            'Q29529315', 'Q887210', 'Q878313', 'Q880198', 'Q29529370', 'Q5589655', 'Q500406', 'Q878260', 'Q3112719',
            'Q878602', 'Q16147601', 'Q578733', 'Q878594', 'Q878628', 'Q4151335', 'Q878605', 'Q878620', 'Q3506352',
            'Q878623', 'Q693032', 'Q878575', 'Q887117', 'Q887117', 'Q5589680', 'Q888386', 'Q5589682', 'Q878657',
            'Q29529184', 'Q886943', 'Q878613', 'Q878585', 'Q878598', 'Q5589687', 'Q878617', 'Q3112728', 'Q886931',
            'Q17089908', 'Q367079', 'Q2347975', 'Q845547', 'Q16202700', 'Q878647', 'Q3773741', 'Q888375', 'Q878581',
            'Q2550683', 'Q887344', 'Q16149111', 'Q887224', 'Q879318', 'Q20765611', 'Q878609', 'Q3773752', 'Q879269',
            'Q2626318', 'Q878640', 'Q5589724', 'Q878326', 'Q5589725', 'Q878323', 'Q15718082', 'Q3773745', 'Q886950',
            'Q878942', 'Q887234', 'Q878264', 'Q878590', 'Q3112727', 'Q886959', 'Q887205', 'Q11250358', 'Q888821',
            'Q5190572', 'Q888795', 'Q888807', 'Q456951', 'Q16197464', 'Q888236', 'Q390720', 'Q6572105', 'Q885934',
            'Q1542521', 'Q2483184', 'Q3128423', 'Q24057525', 'Q35073', 'Q35073', 'Q5296', 'Q5296']
from SPARQLWrapper import SPARQLWrapper, JSON
from fake_useragent import UserAgent

headers_dict = {}
names = []
'''
for i in searcher:
    try:
        sparql = SPARQLWrapper("http://query.wikidata.org/sparql", agent=UserAgent().random)
        sparql.setQuery("""
            SELECT ?inception WHERE {
              wd:%s wdt:P31 ?inception
            }
        """ % i)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        humanity = results['results']['bindings'][0]['inception']['value']

        if humanity == 'http://www.wikidata.org/entity/Q5':
            print('УРА МЕШОК С КОСТЯМИ КОЖАНЫЙ %s' % i)
            names.append(i)
            sparql = SPARQLWrapper("http://query.wikidata.org/sparql", agent=UserAgent().random)
            sparql.setQuery("""
                        SELECT ?inception WHERE {
                          wd:%s wdt:P1559 ?inception
                        }
                    """ % i)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            print(results['results']['bindings'][0]['inception']['value'])

            sparql = SPARQLWrapper("http://query.wikidata.org/sparql", agent=UserAgent().random)
            sparql.setQuery("""
                                        SELECT ?item ?itemLabel 
                                        WHERE 
                                        {
                                          wd:%s wdt:P39 ?item.
                                          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                                        }
                                    """ % i)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            print(results)
            for j in range(0, len(results['results']['bindings'])):
                main_elem = results['results']['bindings'][j]['item']['value']
                result = re.split('/', main_elem)[-1]
                headers_dict[i] = result
        else:
            print('ЭТО НЕ ХУЙНЯ НО И НЕ МЕШОК %s' % i)

    except IndexError:
        print('Это хуйня ' + i)

print(names)

names = ['Q170581', 'Q516515', 'Q766866', 'Q24313', 'Q529294', 'Q355522', 'Q380900', 'Q22686', 'Q24313', 'Q11153', 'Q11142', 'Q11124', 'Q11138', 'Q11107', 'Q11105', 'Q15488345', 'Q4962244', 'Q29863844', 'Q23', 'Q35171', 'Q22686', 'Q6279', 'Q11869', 'Q11896', 'Q91', 'Q35041', 'Q9588', 'Q11881', 'Q9582', 'Q203433', 'Q11237', 'Q178903', 'Q11812', 'Q23', 'Q11806', 'Q11806', 'Q11812', 'Q11812', 'Q179090', 'Q201646', 'Q11813', 'Q219797', 'Q11815', 'Q11816', 'Q11817', 'Q11820', 'Q11820', 'Q109463', 'Q11869', 'Q11869', 'Q11881', 'Q11881', 'Q11896', 'Q11896', 'Q12306', 'Q12306', 'Q12312', 'Q12325', 'Q91', 'Q273546', 'Q8612', 'Q8612', 'Q310852', 'Q313302', 'Q35171', 'Q35678', 'Q35171', 'Q310839', 'Q35041', 'Q310841', 'Q33866', 'Q33866', 'Q35648', 'Q34296', 'Q36023', 'Q36023', 'Q35236', 'Q271023', 'Q298991', 'Q9588', 'Q209989', 'Q9588', 'Q203433', 'Q9582', 'Q9582', 'Q11237', 'Q23685', 'Q49216', 'Q9960', 'Q49214', 'Q1124', 'Q19673', 'Q48259', 'Q76', 'Q6279', 'Q22686', 'Q24313', 'Q6279', 'Q10853588', 'Q11816', 'Q8612', 'Q35648', 'Q11817', 'Q23', 'Q11806', 'Q11812', 'Q11813', 'Q11815', 'Q11816', 'Q11817', 'Q11820', 'Q11869', 'Q11869', 'Q11881', 'Q11896', 'Q11896', 'Q12306', 'Q12312', 'Q12325', 'Q91', 'Q8612', 'Q35171', 'Q35678', 'Q35171', 'Q35041', 'Q33866', 'Q35648', 'Q34296', 'Q36023', 'Q35236', 'Q9588', 'Q9582', 'Q23685', 'Q9960', 'Q1124', 'Q76', 'Q22686', 'Q6279']

print(headers_dict)
'''

names = ['Q22686', 'Q7996', 'Q7747', 'Q185152']
headers_dict = {}
names = ['Q7747']
'''
for i in names:
    headers_dict[i] = []
    temp = i
    sparql = SPARQLWrapper("http://query.wikidata.org/sparql", agent=UserAgent().random)
    sparql.setQuery("""
                                            SELECT ?item ?itemLabel 
                                            WHERE 
                                            {
                                              wd:%s wdt:P39 ?item.
                                              SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                                            }
                                        """ % temp)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    results = results['results']['bindings'][0]['item']['value']
    temp = re.split('/', results)[-1]

    header_pattern = re.compile(r'head|ruler')

    found = False
    for j in range(0,10):
        try:
            sparql = SPARQLWrapper("http://query.wikidata.org/sparql", agent=UserAgent().random)
            sparql.setQuery("""
                                                    SELECT ?item ?itemLabel 
                                                    WHERE 
                                                    {
                                                      wd:%s wdt:P279 ?item.
                                                      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                                                    }
                                                """ % temp)
            print(temp)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            for j in results['results']['bindings']:
                title = j['itemLabel']['value']
                print(title)
                match = re.match(header_pattern, title)
                print(match)
                if match:
                    found = True
                    break
            if found:
                headers_dict[i].append(temp)
                break
            temp = re.split('/', results['results']['bindings'][0]['item']['value'])[-1]
        except IndexError:
            break
            
            
final_headers_dict = {}
for i in headers_dict:
    if headers_dict[i]:
        final_headers_dict[i] = headers_dict[i]
'''


def get_title(id):
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

def get_subclass(id):
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


for i in names:
    try:
        headers_dict[i] = []
        temp = 'Q7747'
        results = get_title(temp)
        title_list = []
        for k in results['results']['bindings']:
            results = k['item']['value']
            main_title = re.split('/', results)[-1]
            title_list.append(main_title)
        print(title_list)
        for point in title_list:
            header_pattern = re.compile(r'head|ruler')
            found = False

            results = get_subclass(point)
            current_list = []
            print(results)
            for k in results['results']['bindings']:
                results = k['item']['value']
                print(results)
                current_title = re.split('/', results)[-1]
                match = re.match(header_pattern, current_title)
                if match:
                    headers_dict[i].append(point)
                    break
                current_list.append(current_title)

            results = get_subclass(point)
            current_list_second = []
            for m in current_list:
                results = m['item']['value']
                current_title_second = re.split('/', results)[-1]
                match = re.match(header_pattern, current_title_second)
                if match:
                    headers_dict[i].append(point)
                    break
            print('Конец цикла')
    except IndexError:
        None
print(headers_dict)
# print(final_headers_dict)
