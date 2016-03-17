import json
import os

with open(os.environ['PYTHONPATH']+'/resource/36kr_city.json', 'r') as f:
    datas = json.load(f, encoding='utf8')

city_dicts = {}
print datas[0]
for data in datas:
    city_dicts[data['id']] = data

print len(city_dicts)
for (key, city) in city_dicts.items():
    print key, city
