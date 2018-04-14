import os
import subprocess
import csv
import sqlalchemy as db

import formWikiGraph as make_graph

engine = db.create_engine('postgres://vis:wikivis@192.168.10.105:5432')
metadata = db.MetaData(engine)

articles = db.Table('articles', metadata,
                    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
                    db.Column('name', db.String(256), nullable=False, unique=True))

links = db.Table('hierarchy_links', metadata,
                 db.Column('id', db.Integer, primary_key=True, autoincrement=True),
                 db.Column('link_from', db.ForeignKey('articles.id'), nullable=False),
                 db.Column('link_to', db.ForeignKey('articles.id'), nullable=False),
                 db.Column('num_refs', db.Integer, nullable=True))

metadata.create_all( engine )

conn = engine.connect()

print( "Creating graph" )
make_graph.formWikiGraphFromTitles()

articles_ins = articles.insert()

conn = engine.connect()

char = ""

broken_graph = {}

acounter = 0
aqueue = []
alen = len(make_graph.WIKI_GRAPH.keys())

for a in make_graph.WIKI_GRAPH.keys():
    aqueue.append({'name': a})
    acounter += 1
    if acounter % 1000 == 0:
        print( "    Added %i out of %i articles (%f%%)" % (acounter, alen, (float(acounter)/alen) * 100))
        conn.execute( articles_ins, aqueue )
        aqueue = []

"""
print ("Getting list of first chars")
for k in make_graph.WIKI_GRAPH.keys():
    if k[0] in broken_graph:
        broken_graph[k[0]][k] = make_graph.WIKI_GRAPH[k]
    else:
        broken_graph[k[0]] = {k: make_graph.WIKI_GRAPH[k]}

print( "Adding all articles at once...." )
for char in chars:
    print( "Adding all articles beginning with " + char)
    conn.execute( articles_ins, [{'name': n} for n in make_graph.WIKI_GRAPH.keys() if n[0] == char] )
"""
links_ins = links.insert()

insert_queue = []

counter = 0
bcounter = 0

for filename in os.listdir('data/'):
    if filename.endswith('.tsv'):
        filelen = int(subprocess.check_output(['wc', '-l', 'data/' + filename]).decode('utf-8').split(' ')[0])
        print( "Opened file with %i entries" % (filelen))
        with open('data/' + filename) as tsv:
            for line in csv.reader( tsv, dialect='excel-tab' ):
                if (not line[2] == 'external') and (not line[0].startswith('other-')) and (not line[1].startswith('other-')):
                    get_from = db.select([articles]).where(articles.c.name == line[0])
                    result = conn.execute( get_from )
                    fromval = result.first()

                    get_to = db.select([articles]).where(articles.c.name == line[1])
                    result = conn.execute( get_to )
                    toval = result.first()

                    if fromval and toval:
                        insert_queue.append({'link_from': fromval['id'], 'link_to': toval['id'], 'num_refs': int(line[3])})
                        counter += 1
                        if counter % 500 == 0:
                            if insert_queue:
                                conn.execute( links_ins, insert_queue )
                                del insert_queue
                                insert_queue = []
                            print( '    Added or discarded %i of %i entries (%f%%)' % (bcounter, filelen, (float(bcounter)/filelen) * 100) )
                bcounter += 1;



"""
nlinks = []

incr = 1

now_go = False

bkeys = list(broken_graph)
for c in bkeys:
    if now_go:
        print( "Linking all articles beginning with %s: %i out of %i, with %i entries" % (c, incr, len(bkeys), len(broken_graph[c].keys())))
        print ( "  Getting links...." )
        make_graph.addLinksToGraph( broken_graph[c], len(broken_graph[c].keys()))
        print ( "  Adding links to database...." )
        for aname in broken_graph[c]:
            if broken_graph[c][aname]:
                sname = db.select([articles]).where(articles.c.name == aname)
                result = conn.execute( sname )
                aname_id = result.first()
                if aname_id and aname_id['id']:
                    for ato in broken_graph[c][aname]:
                        sto = db.select([articles]).where(articles.c.name == ato)
                        result = conn.execute( sto )
                        ato_id = result.first()
                        if ato_id and ato_id['id']:
                            nlinks.append({'link_from': aname_id['id'], 'link_to': ato_id['id']})
        if nlinks:
            conn.execute( links_ins, nlinks )
        del nlinks
        nlinks = []
        incr += 1
        del broken_graph[c]
    else:
        if c == '0':
            now_go = True
"""


