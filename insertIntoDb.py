import os
import csv
import sqlalchemy as db

import formWikiGraph as make_graph

engine = db.create_engine('postgres://vis:wikivis@130.64.128.179:5432')
metadata = db.MetaData(engine)

articles = db.Table('articles', metadata,
                    db.Column('id', db.Integer, db.Sequence('articles_id_seq'), primary_key=True),
                    db.Column('name', db.String(256), nullable=False, unique=True))

links = db.Table('hierarchy_links', metadata,
                 db.Column('id', db.Integer, db.Sequence('hierarchy_links_id_seq'), primary_key=True),
                 db.Column('link_from', db.ForeignKey('articles.name'), nullable=False),
                 db.Column('link_to', db.ForeignKey('articles.name'), nullable=False),
                 db.Column('num_refs', db.Integer, nullable=True))

metadata.create_all( engine )

make_graph.formWikiGraphFromTitles()

articles_ins = articles.insert()
links_ins = links.insert()

conn = engine.connect()

for aname in make_graph.WIKI_GRAPH:
    conn.execute( articles_ins, name=aname )

make_graph.addLinksToGraph()

for aname in make_graph.WIKI_GRAPH:
    if len(make_graph.WIKI_GRAPH[aname]) > 0:
        sname = db.select([articles]).where(articles.c.name == aname)
        result = conn.execute( sname )
        aname_id = result.first()['id'] 
        for ato in make_graph.WIKI_GRAPH[aname]:
            sto = db.select([articles]).where(articles.c.name == ato)
            result = conn.execute( sto )
            print( "Crossing " + aname + " with " + ato)
            ato_id = result.first()['id']
            conn.execute( links_ins, link_from=aname_id, link_to=ato_id )

#for filename in os.listdir('data/'):
#    with open filename as tsv:
#        for line in csv.reader( tsv, dialect='excel-tab' ):
#            slinks = db.select(
