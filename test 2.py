from SPARQLWrapper import SPARQLWrapper, JSON
from fake_useragent import UserAgent

headers_dict = {}

names = ['Q170581', 'Q516515', 'Q766866', 'Q24313', 'Q529294', 'Q355522', 'Q380900', 'Q22686', 'Q24313', 'Q11153', 'Q11142', 'Q11124']
# 'Q11138', 'Q11107', 'Q11105', 'Q15488345', 'Q4962244', 'Q29863844', 'Q23', 'Q35171', 'Q22686', 'Q6279', 'Q11869', 'Q11896', 'Q91', 'Q35041', 'Q9588', 'Q11881', 'Q9582', 'Q203433', 'Q11237', 'Q178903', 'Q11812', 'Q23', 'Q11806', 'Q11806', 'Q11812', 'Q11812', 'Q179090', 'Q201646', 'Q11813', 'Q219797', 'Q11815', 'Q11816', 'Q11817', 'Q11820', 'Q11820', 'Q109463', 'Q11869', 'Q11869', 'Q11881', 'Q11881', 'Q11896', 'Q11896', 'Q12306', 'Q12306', 'Q12312', 'Q12325', 'Q91', 'Q273546', 'Q8612', 'Q8612', 'Q310852', 'Q313302', 'Q35171', 'Q35678', 'Q35171', 'Q310839', 'Q35041', 'Q310841', 'Q33866', 'Q33866', 'Q35648', 'Q34296', 'Q36023', 'Q36023', 'Q35236', 'Q271023', 'Q298991', 'Q9588', 'Q209989', 'Q9588', 'Q203433', 'Q9582', 'Q9582', 'Q11237', 'Q23685', 'Q49216', 'Q9960', 'Q49214', 'Q1124', 'Q19673', 'Q48259', 'Q76', 'Q6279', 'Q22686', 'Q24313', 'Q6279', 'Q10853588', 'Q11816', 'Q8612', 'Q35648', 'Q11817', 'Q23', 'Q11806', 'Q11812', 'Q11813', 'Q11815', 'Q11816', 'Q11817', 'Q11820', 'Q11869', 'Q11869', 'Q11881', 'Q11896', 'Q11896', 'Q12306', 'Q12312', 'Q12325', 'Q91', 'Q8612', 'Q35171', 'Q35678', 'Q35171', 'Q35041', 'Q33866', 'Q35648', 'Q34296', 'Q36023', 'Q35236', 'Q9588', 'Q9582', 'Q23685', 'Q9960', 'Q1124', 'Q76', 'Q22686', 'Q6279']
for i in names:

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

        print(results['results']['bindings'][j]['itemLabel']['value'])
