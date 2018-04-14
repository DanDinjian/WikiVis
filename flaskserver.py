from flask import *
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://vis:wikivis@130.64.128.179:5432'

db = SQLAlchemy(app)

WIKI_LINKS_URL = "https://en.wikipedia.org/w/api.php?action=query&prop=links&pllimit=max&format=json&redirects=true&titles="

from models import *

@app.before_first_request
def setup():
    db.reflect()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/wikiviz')
def view_vis():
    return render_template("wikiviz.html")

@app.route('/api/hierarchy/<string:name>', methods=['GET'])
def get_hierarchy_links(name):
    links = []
    url = WIKI_LINKS_URL + name
    data = requests.get(url).json()
    if 'query' in data and not 'redirects' in data['query']:
        pageid = list(data['query']['pages'])[0]
        links_as_dictlist = data['query']['pages'][pageid]['links']
        for d in links_as_dictlist:
            links.append({'name': d['title'].replace(' ', '_')} )
    return jsonify(links)

@app.route('/api/clickstream/from/<string:aname>', methods=['GET'])
def get_clickstream_links(aname):
    links = []
    root = Article.query.filter_by(name=aname).first()
    leaves = ClickstreamLink.query.filter_by(link_to=root.id)

    for l in leaves:
        leaf = Article.query.filter_by(id=l.id).first()
        print( leaf )
        links.append({'name': leaf.name, 'num_refs': l.num_refs})

    return jsonify(links)

@app.route('/api/clickstream/to/<string:aname>', methods=['GET'])
def get_clickstream_to(aname):
    links = []
    root = Article.query.filter_by(name=aname).first()
    sources = ClickstreamLink.query.filter_by(link_from=root.id)

    for s in sources:
        source = Article.query.filter_by(id=s.id).first()
        links.append({'name': source.name, 'num_refs': s.num_refs })

    return jsonify(links)

if __name__ == '__main__':
    app.run(debug=True)
