import os
import csv
import sqlalchemy as db

import formWikiGraph as make_graph

engine = db.create_engine('test')
metadata = db.MetaData(engine)

articles = db.Table('articles', metadata,
                    db.Column('id', db.Integer, db.Sequence('articles_id_seq'), primary_key=True),
                    db.Column('name', db.String(256), nullable=False))

links = db.Table('hierarchy_links', metadata,
                 db.Column('id', db.Integer, db.Sequence('hierarchy_links_id_seq'), primary_key=True),
                 db.Column('from', db.ForeignKey('articles.name'), nullable=False),
                 db.Column('to', db.ForeignKey('articles.name'), nullable=False),
                 db.Column('num_refs', db.Integer, nullable=True))

metadata.create_all( engine )

make_graph.formWikiGraphFromTitles()
make_graph.addLinksToGraph()

articles_ins = articles.insert()
links_ins = links.insert()

conn = engine.connect()

for aname in make_graph.WIKI_GRAPH:
    conn.execute( articles_ins, name=aname )

for aname in make_graph.WIKI_GRAPH:
    sname = db.select(articles).where(articles.c.id == aname)
    result = conn.execute( sname )
    aname_id = result.fetchone()['id']
    for ato in make_graph.WIKI_GRAPH[aname]:
        sto = db.select(articles).where(articles.c.id == ato)
        result = conn.execute( sto )
        ato_id = result.fetchone()['id']
        conn.execute( links_ins, from=aname_id, to=ato_id )

#for filename in os.listdir('data/'):
#    with open filename as tsv:
#        for line in csv.reader( tsv, dialect='excel-tab' ):
#            slinks = db.select(
