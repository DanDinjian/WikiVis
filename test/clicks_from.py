import requests

url = "http://127.0.0.1:5000"

clicks = requests.get(url + "/api/clickstream/from/Aristotle")

for c in clicks.json():
    print( "%s %s" % (c['num_refs'], c['name']))
