from flask import *
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
#import psycopg2 as dbr
import requests
from flask_bootstrap import Bootstrap

import cProfile
import io as StringIO
import pstats
import contextlib

@contextlib.contextmanager
def profiled():
    pr = cProfile.Profile()
    pr.enable()
    yield
    pr.disable()
    s = StringIO.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats()
    # uncomment this to see who's calling what
    # ps.print_callers()
    print(s.getvalue())


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://vis:wikivis@130.64.128.179:5432'
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

Bootstrap(app)

SERVER_NAME = "http://127.0.0.1:5000/"

db = SQLAlchemy(app)

from models import *

#dbparams = {"database": "vis", "user": "vis", "password": "wikivis", "host": "130.64.128.179", "port": 5432}
#conn = dbr.connect(**dbparams)

WIKI_LINKS_URL = "https://en.wikipedia.org/w/api.php?action=query&prop=links&pllimit=max&format=json&redirects=true&titles="

class ReusableForm(Form):
    article = TextField('Search:', validators=[validators.required()], render_kw={"placeholder": "article name"})


@app.before_first_request
def setup():
    db.reflect()

@app.route('/', methods=['GET', 'POST'])
def home():
    form = ReusableForm(request.form)
    print(form.errors)
    results = []
    if request.method == 'POST':
        article=request.form['article']
        results_to = get_clickstream_to(article)
        results_from = get_clickstream_from(article)
        if form.validate():
            # Save the comment here.
            flash('You searched for ' + article)
        else:
            flash('All the form fields are required. ')
        return render_template("wikiviz.html", form=form, results_to=results_to, results_from=results_from)

    else:
        return render_template("index.html", form=form)

@app.route('/wikiviz', methods=['GET', 'POST'])
def wikivizpage():
    form = ReusableForm(request.form)
    print(form.errors)
    results = []
    if request.method == 'POST':
        article=request.form['article']
        results_to = get_clickstream_to(article)
        results_from = get_clickstream_from(article)
        if form.validate():
            # Save the comment here.
            flash('You searched for ' + article)
        else:
            flash('All the form fields are required. ')
        return render_template("wikiviz.html", results_to=results_to, results_from=results_from, form=form, article=article)
    else:
        return render_template("wikiviz.html", form=form, results_to=[], results_from=[])
    # return render_template("wikiviz.html", form=form)

@app.route('/wikiviz_w_data', methods=['GET', 'POST'])
def view_vis():
    form = ReusableForm(request.form)
    print(form.errors)
    results = []
    if request.method == 'POST':
        article=request.form['article']
        results = get_clickstream_to(article)

        if form.validate():
            # Save the comment here.
            flash('You searched for ' + article)
        else:
            flash('All the form fields are required. ')
    return render_template("wikiviz_w_data.html", results=results, form=form)

@app.route('/api/hierarchy/<string:name>', methods=['GET'])
def hierarchy_api(name):
    return jsonify(get_hierarchy_links(name))

def get_hierarchy_links(name):
    links = []
    suffix = ""
    while True:
        url = WIKI_LINKS_URL + name + suffix
        data = requests.get(url).json()
        with open("output.txt", 'w') as fp:
            fp.write( str(data) )
        if 'query' in data and not 'redirects' in data['query']:
            pageid = list(data['query']['pages'])[0]
            links_as_dictlist = data['query']['pages'][pageid]['links']
            for d in links_as_dictlist:
                links.append({'name': '_'.join(d['title'].split())} )
        if 'continue' in data:
            suffix = "&plcontinue=" + data['continue']['plcontinue']
        else:
            break
    return links

@app.route('/api/clickstream/to/<string:aname>', methods=['GET'])
def request_clickstream_to(aname):
    return jsonify(get_clickstream_to(aname))


def get_clickstream_to(aname):
    links = []
    aname = '_'.join(aname.split())
    print("Getting \"to\" links from " + aname)
    marticle = Article.query.filter(db.func.lower(Article.name) == db.func.lower(aname)).first()
    subq = ClickstreamLink.query.filter(ClickstreamLink.link_from == marticle.id).limit(1000).all()
    for q in subq:
        leaf = Article.query.filter(Article.id == q.link_to).first()

        links.append({'name': leaf.name, 'num_refs': q.num_refs})

    return links

@app.route('/api/clickstream/from/<string:aname>', methods=['GET'])
def request_clickstream_from(aname):
    return jsonify(get_clickstream_from(aname))


def get_clickstream_from(aname):
    links = []
    aname = '_'.join(aname.split())
    print("Getting \"from\" links from " + aname)
    marticle = Article.query.filter(db.func.lower(Article.name) == db.func.lower(aname)).first()
    subq = ClickstreamLink.query.filter(ClickstreamLink.link_to == marticle.id).limit(1000).all()
    for q in subq:
        leaf = Article.query.filter(Article.id == q.link_from).first()

        links.append({'name': leaf.name, 'num_refs': q.num_refs})

    return links

if __name__ == '__main__':
    app.run(threaded=True, debug=True)
