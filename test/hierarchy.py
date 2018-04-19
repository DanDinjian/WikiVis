import requests

url = "http://127.0.0.1:5000"

hierarchy = requests.get(url + "/api/hierarchy/Aristotle");

for item in hierarchy.json():
    print( item['name'] );
