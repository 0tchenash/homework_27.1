from ads.models import Ad
import json

with open("ad.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

for ad in data:
    u = Ad(**ad)
    u.save()

#################

from ads.models import Category
import json
with open("category.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

for cat in data:
    u = Category(**cat)
    u.save()

#################

from users.models import Location
import json

with open("location.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for loc in data:
    u = Location(**loc)
    u.save()

######################

from users.models import User
import json

with open("user.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for user in data:
    u = User(**user)
    u.save()

   