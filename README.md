load data into file data/english-wiki-titles
get title dump from http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-all-titles-in-ns0.gz

load clickstream data into file data/2017_en_clickstream.tsv
https://ndownloader.figshare.com/files/7563832

To change the database insertIntoDb.py references, update the first parameter of db.create_engine().
The current database is hosted at: "postgres://vis:wikivis@130.64.128.179:5432"
Username: "vis"
Password: "wikivis"

Three API paths:
'/api/hierarchy/<aname>'
    -- Gets Wikipedia's official list of related links for a given article
    -- aname: name of the desired Wikipedia article
    -- Returns a list of {'name': <article name>} objects

'/api/clickstream/from/<aname>'
    -- Gets a list of all articles FROM which users traversed TO the given article
    -- aname: name of the desired "destination" Wikipedia article
    -- Returns a list of {'name': <article name>, 'num_refs': <number of times users followed this path>} objects

'/api/clickstream/to<aname>'
    -- Gets a list of all articles TO which users traversed FROM the given article
    -- aname: name of the desired "source" Wikipedia article
    -- Returns the same data type as the "from" path
