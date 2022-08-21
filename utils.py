import csv
import json
with open('ads.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    for row in rows:
        if row['is_published'] == 'TRUE':
            row['is_published'] = True
        else:
            row['is_published'] = False 
with open('ads.json', 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=False, indent=4)

with open('categories.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
with open('categories.json', 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=False, indent=4)