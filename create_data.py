from ads.models import Ads, Categories
import json

with open("ads.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

for ad in data:
    u = Ads(**ad)
    u.save()

#################

from ads.models import Categories
import json
with open("categories.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

for cat in data:
    u = Categories(**cat)
    u.save()
