import csv
import json



with open('india.csv','r',encoding='utf-8') as csv_file:
    rows = csv.reader(csv_file)
    out = {}
    for row in rows:
        out[row[0]] = dict(zip(row[0].split('+'),row[1].split('+')))
    with open('my_new_dict.json','w',encoding='utf-8') as json_file:
        json.dump(out,json_file,indent=4,ensure_ascii=False)