load data into file data/english-wiki-titles
get title dump from http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-all-titles-in-ns0.gz

load clickstream data into file data/2017_en_clickstream.tsv
https://ndownloader.figshare.com/files/7563832

To change the database insertIntoDb.py references, update the first parameter of db.create_engine().
The current database is hosted at: "postgres://vis:wikivis@130.64.128.179:5432"
Username: "vis"
Password: "wikivis"
