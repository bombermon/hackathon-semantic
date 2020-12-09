import csv

table = {'Q40787': ['Q11696', 'Emperor of All Russia', '01.11.1894', '15.03.1917', '0', '0'], 'Q7747': ['Q60497063', 'President of Russia', '07.05.2012', 'по наст. время', '0', '0'], 'Q7996': ['Q11696', 'Tsar of Russia', '16.01.1547', '1.01.1575', '0', '2'], 'Q22686': ['Q11696', 'President of the United States', '07.01.2020', 'по наст. время', '0', '0']}


temp_table = {}

def save_data(file_name, data):
    table_rows = []
    temp_row = {"person": '', "position": '', "start_precision": '', "start": '', "end_precision": '', "end": ''}
    for i in data.keys():
        current_row = temp_row
        current_row["person"] = "https://www.wikidata.org/wiki/" + i
        current_row["position"] = "https://www.wikidata.org/wiki/" + data[i][0]
        current_row["start_precision"] = data[i][4]
        current_row["start"] = data[i][2]
        current_row["end_precision"] = data[i][5]
        current_row["end"] = data[i][3]
        table_rows.append(current_row.copy())
    with open(file_name + '.csv', 'w', encoding='UTF-8') as csv_file:  # ОТКРЫВАЕМ (ИЛИ СОЗДАЕМ ФАЙЛ CSV НА ЗАПИСЬ СЛОВАРЯ)
        writer = csv.DictWriter(csv_file, fieldnames = temp_row.keys())
        writer.writeheader()
        writer.writerows(table_rows)

save_data("sample", table)]