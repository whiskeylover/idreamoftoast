import datetime
import json
import urllib2

from flask import Flask, jsonify, Response
from flask import render_template
from peewee import Model, SqliteDatabase
from peewee import CharField, DateTimeField, IntegerField

#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------
MAX_TOP_DREAMS = 8
EXTERNAL_RESOURCE_REFRESH_FREQ = 30
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
    
    picURL = CharField(null=True)
    picURLthn = CharField(null=True)
    definition = CharField(null=True)
    
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
    dreams = Dream.select().where(Dream.count > 0).order_by(order)[:limit]
    return [{'name':d.name, 'count':d.count, 'definition': d.definition, 'picURL': d.picURL, 'picURLthn': d.picURLthn} for d in dreams]

def get_dream(dream):
    """ Helper method for getting a single dream. """
    d = Dream.select().where(Dream.name == dream).first()
    
    if d is None:
        d = Dream.create(name=dream.lower(), count=0, picURL=get_flickrpicURL(dream), picURLthn=get_flickrpicURL(dream), definition=get_urbandictionary(dream))
        
    return {'name':d.name, 'count':d.count, 'definition': d.definition, 'picURL': d.picURL, 'picURLthn': d.picURLthn}

#-------------------------------------------------------------------------------
# Routes / Controllers
#-------------------------------------------------------------------------------
@app.route("/dream/define/<term>")
def get_urbandictionary(term):
    try:
        response = urllib2.urlopen('http://api.urbandictionary.com/v0/define?term=' + term.replace(" ", "+"))
        html = response.read()

        j = json.loads(html)
        
        print "Refreshed " + term + "'s definition"
        
        return j['list'][0]['definition']
    except:
        return ""

@app.route("/dream/picURL/<term>")
def get_flickrpicURL(term):
    api_key = 'b60ce2a4db0b09dc4e9e895efe6d660e'
    URL = 'http://api.flickr.com/services/rest/?method=flickr.photos.search&' + \
        'api_key=' + api_key + \
        '&tags=' + term.replace(" ", "+") + \
        '&privacy_filter=1&format=json&nojsoncallback=1'

    try:
        response = urllib2.urlopen(URL)
        html = response.read()
        j = json.loads(html)
 
        print "Refreshed " + term + "'s picURL"
        
        return "http://farm{0}.staticflickr.com/{1}/{2}_{3}_z.jpg".format( \
            j['photos']['photo'][0]['farm'], \
            j['photos']['photo'][0]['server'], \
            j['photos']['photo'][0]['id'], \
            j['photos']['photo'][0]['secret'])

    except:
        return "assets/img/888888.png"

@app.route("/dream/picURLthn/<term>")
def get_flickrpicURLthn(term):
    api_key = 'b60ce2a4db0b09dc4e9e895efe6d660e'
    URL = 'http://api.flickr.com/services/rest/?method=flickr.photos.search&' + \
        'api_key=' + api_key + \
        '&tags=' + term.replace(" ", "+") + \
        '&privacy_filter=1&format=json&nojsoncallback=1'

    try:
        response = urllib2.urlopen(URL)
        html = response.read()
        j = json.loads(html)
 
        print "Refreshed " + term + "'s picURLthn"
        
        return "http://farm{0}.staticflickr.com/{1}/{2}_{3}_q.jpg".format( \
            j['photos']['photo'][0]['farm'], \
            j['photos']['photo'][0]['server'], \
            j['photos']['photo'][0]['id'], \
            j['photos']['photo'][0]['secret'])

    except:
        return "assets/img/888888thn.png"

   
@app.route("/dreams/add/<dream>")
def add_dream(dream):
    d = Dream.get_or_create(name=dream.lower())
    d.count += 1
    
    # if the record has just been created, fetch the picURL and definition
    if d.count == 1:
        print "Creating new dream"
        d.created_on = datetime.datetime.now()
        d.modified_on = datetime.datetime.now()
        d.picURL = get_flickrpicURL(d.name)
        d.picURLthn = get_flickrpicURLthn(d.name)
        d.definition = get_urbandictionary(d.name)
    else:
        print "Fetching existing dream"
        
    # if the definition and URL are more than EXTERNAL_RESOURCE_REFRESH_FREQ days old
    days_old = 0
    try:
        days_old = (d.modified_on - d.created_on).days
    except:
        days_old = 0

    if days_old >= EXTERNAL_RESOURCE_REFRESH_FREQ:
        d.picURL = get_flickrpicURL(d.name)
        d.picURLthn = get_flickrpicURLthn(d.name)
        d.definition = get_urbandictionary(d.name)
        d.modified_on = datetime.datetime.now()
        
    d.save()
    return jsonify(data={'id': d.id,
                         'count': d.count})

@app.route("/dreams/top")
def top_dreams():
    a = get_dreams(Dream.count.desc(), MAX_TOP_DREAMS)
    return Response(json.dumps(a),  mimetype='application/json')

    #return jsonify(data=get_dreams(Dream.count.desc(), MAX_TOP_DREAMS))

@app.route("/dreams/recent")
def recent_dreams():
    a = get_dreams(Dream.modified_on.desc(), MAX_TOP_DREAMS)
    return Response(json.dumps(a),  mimetype='application/json')

    #return jsonify(data=get_dreams(Dream.modified_on.desc(), MAX_TOP_DREAMS))

@app.route("/dreams/get/<dream>")
def get_single_dream(dream):
    a = get_dream(dream)
    return Response(json.dumps(a), mimetype='application/json')

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    # Development only! Reloads server on file change.
    init_db()
    app.debug = True
    app.run()
