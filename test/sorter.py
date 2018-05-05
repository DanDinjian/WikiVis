import sys
import json

with open(sys.argv[1], 'r') as fp:
    rawdata = fp.read()

data = json.loads(rawdata)

sdata = sorted(data, key=lambda i: i['num_refs'])

for s in sdata:
    print("%s %s" % (s['num_refs'], s['name']))
