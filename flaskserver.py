from flask import *
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
import requests
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://vis:wikivis@130.64.128.179:5432'
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

Bootstrap(app)

SERVER_NAME = "http://127.0.0.1:5000/"

db = SQLAlchemy(app)

WIKI_LINKS_URL = "https://en.wikipedia.org/w/api.php?action=query&prop=links&pllimit=max&format=json&redirects=true&titles="

from models import *

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
        #results_to = get_clickstream_to(article)
        results_from = get_clickstream_to(article)
        if form.validate():
            # Save the comment here.
            flash('You searched for ' + article)
        else:
            flash('All the form fields are required. ')
        return render_template("wikiviz.html", form=form, results=results_from)

    else:
        return render_template("index.html", form=form)

@app.route('/wikiviz', methods=['GET', 'POST'])
def wikivizpage():
    form = ReusableForm(request.form)
    print(form.errors)
    results = []
    if request.method == 'POST':
        article=request.form['article']
        print(article)
        results_to = get_clickstream_to(article)
        print(results_to)
        results_from = get_clickstream_from(article)
        print(results_from)
        if form.validate():
            # Save the comment here.
            flash('You searched for ' + article)
        else:
            flash('All the form fields are required. ')
        return render_template("wikiviz.html", results1=results_to, results2=results_from, form=form, article=article)
    else:
        return render_template("wikiviz.html", form=form, results1=[], results2=[])
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
                links.append({'name': d['title'].replace(' ', '_')} )
        if 'continue' in data:
            suffix = "&plcontinue=" + data['continue']['plcontinue']
        else:
            break
    return links

@app.route('/api/clickstream/to/<string:aname>', methods=['GET'])
def clickstream_to_api(aname):
    return jsonify(get_clickstream_to(aname))

def get_clickstream_to(aname):
    aname = aname.replace(" ", "_")
    links = []
    subq = db.session.query(ClickstreamLink.link_from, ClickstreamLink.num_refs).join(Article, db.and_(Article.id == ClickstreamLink.link_to, Article.name == aname)).subquery('subq')
    leaves = db.session.query(Article.name, subq.c.num_refs).join(subq, subq.c.link_from == Article.id)
    
    for l in leaves:
        links.append({'name': l[0], 'num_refs': l[1]})
    
    return links

@app.route('/api/clickstream/from/<string:aname>', methods=['GET'])
def clickstream_from_api(aname):
    return jsonify(get_clickstream_from(aname))

def get_clickstream_from(aname):
    links = []
    subq = db.session.query(ClickstreamLink.link_to, ClickstreamLink.num_refs).join(Article, db.and_(Article.id == ClickstreamLink.link_from, Article.name == aname)).subquery('subq')
    sources = db.session.query(Article.name, subq.c.num_refs).join(subq, subq.c.link_to == Article.id)
    
    for s in sources:
        links.append({'name': s[0], 'num_refs': s[1]})

    return links

if __name__ == '__main__':
    app.run(debug=True)
