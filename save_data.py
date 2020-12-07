import csv

table = {'QPERSON': ['QPOSITION', 'Name_Of_Position', 'Start',  'end', 'level_start', 'end_level'],
         'asdf': ['QPasdfON', 'Namasdfsition', 'asdf',  'easdad', 'levasdftart', 'end_asdfvel']}

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
    with open(file_name + '.csv', 'w') as csv_file:  # ОТКРЫВАЕМ (ИЛИ СОЗДАЕМ ФАЙЛ CSV НА ЗАПИСЬ СЛОВАРЯ)
        writer = csv.DictWriter(csv_file, fieldnames = temp_row.keys())
        writer.writeheader()
        writer.writerows(table_rows)

save_data("sample", table)