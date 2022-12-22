import lib
import json

data = lib.read_json('data/site.json')

for page in data['results']:
  for href in data['results'][page]:
    if 'ok' not in data['results'][page][href] or not data['results'][page][href]['ok']:
      print(json.dumps(data['results'][page], indent=2))
