import datetime
import json
import urllib2

from flask import Flask, jsonify
from flask import render_template
from peewee import Model, SqliteDatabase
from peewee import CharField, DateTimeField, IntegerField

#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------
MAX_TOP_DREAMS = 5

#-------------------------------------------------------------------------------
# Globals
#-------------------------------------------------------------------------------
db = SqliteDatabase('toast.db', threadlocals=True)
app = Flask(__name__)

#-------------------------------------------------------------------------------
# Models
#-------------------------------------------------------------------------------
class Dream(Model):
    """" Dream model. """
    name = CharField()
    count = IntegerField(default=0)
    created_on = DateTimeField(default=datetime.datetime.now)
    modified_on = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

#-------------------------------------------------------------------------------
# Methods
#-------------------------------------------------------------------------------
def init_db():
    """ Initialize database. """
    db.connect()
    if not Dream.table_exists():
        Dream.create_table()

def get_dreams(order, limit):
    """ Helper method for getting dreams. """
    dreams = Dream.select().order_by(order)[:limit]
    return [{'name':d.name, 'count':d.count} for d in dreams]

#-------------------------------------------------------------------------------
# Routes / Controllers
#-------------------------------------------------------------------------------
@app.route("/dream/define/<term>")
def get_urbandictionary(term):
    response = urllib2.urlopen('http://api.urbandictionary.com/v0/define?term=' + term)
    html = response.read()

    j = json.loads(html)
    return j['list'][0]['definition']

@app.route("/dream/picURL/<term>")
def get_flickrpicURL(term):
    api_key = 'b60ce2a4db0b09dc4e9e895efe6d660e'
    URL = 'http://api.flickr.com/services/rest/?method=flickr.photos.search&' + \
        'api_key=' + api_key + \
        '&tags=' + term + \
        '&privacy_filter=1&format=json&nojsoncallback=1'

    response = urllib2.urlopen(URL)
    html = response.read()
    j = json.loads(html)


    return "http://farm{0}.staticflickr.com/{1}/{2}_{3}_z.jpg".format( \
        j['photos']['photo'][0]['farm'], \
        j['photos']['photo'][0]['server'], \
        j['photos']['photo'][0]['id'], \
        j['photos']['photo'][0]['secret'])

@app.route("/dreams/add/<dream>")
def add_dream(dream):
    d = Dream.get_or_create(name=dream)
    d.count += 1
    d.modified_on = datetime.datetime.now()
    d.save()
    return jsonify(data={'id': d.id,
                         'count': d.count})

@app.route("/dreams/top")
def top_dreams():
    return jsonify(data=get_dreams(Dream.count.desc(), MAX_TOP_DREAMS))

@app.route("/dreams/recent")
def recent_dreams():
    return jsonify(data=get_dreams(Dream.modified_on.desc(), MAX_TOP_DREAMS))

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    # Development only! Reloads server on file change.
    init_db()
    app.debug = True
    app.run()
