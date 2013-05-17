import datetime
import json
import os
import urllib2

from flask import Flask, jsonify, Response
from flask import render_template
from peewee import Model, MySQLDatabase, SqliteDatabase
from peewee import CharField, DateTimeField, IntegerField
from urllib import unquote

#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------
MAX_TOP_DREAMS = 8
EXTERNAL_RESOURCE_REFRESH_FREQ = 30

#-------------------------------------------------------------------------------
# Environment
#-------------------------------------------------------------------------------
env = os.environ.get('TOAST_PRODUCTION', None)

# If env is set, we are in production!
if env:
    # Production settings here!
    host = os.environ.get('TOAST_HOST', None)
    user = os.environ.get('TOAST_USER', None)
    passwd = os.environ.get('TOAST_PASSWD', None)
    if not (host or user or passwd):
        import sys
        print 'Environment variables NOT set!'
        sys.exit()
    db = MySQLDatabase('idreamoftoast', host=host, user=user, passwd=passwd)
    app = Flask(__name__)

    import logging
    path = os.environ.get('TOAST_LOG_PATH', './')
    file_handler = logging.FileHandler(path + 'flask.log')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(file_handler)
else:
    # Development settings here!
    db = SqliteDatabase('toast.db', threadlocals=True)
    app = Flask(__name__, static_folder='public', static_url_path='')

    @app.route("/")
    def root():
        return app.send_static_file('index.html')

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
    d = Dream.select().where(Dream.name == dream.lower()).first()

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
    
    d = Dream.get_or_create(name=unquote(dream.lower()))
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
    #Response.headers.add('Access-Control-Allow-Origin', '*')
    return Response(json.dumps(a),  mimetype='application/json', headers={'Access-Control-Allow-Origin': '*'})

    #return jsonify(data=get_dreams(Dream.count.desc(), MAX_TOP_DREAMS))

@app.route("/dreams/recent")
def recent_dreams():
    a = get_dreams(Dream.modified_on.desc(), MAX_TOP_DREAMS)
    return Response(json.dumps(a),  mimetype='application/json', headers={'Access-Control-Allow-Origin': '*'})

    #return jsonify(data=get_dreams(Dream.modified_on.desc(), MAX_TOP_DREAMS))

@app.route("/dreams/get/<dream>")
def get_single_dream(dream):
    a = get_dream(unquote(dream.lower()))
    return Response(json.dumps(a), mimetype='application/json', headers={'Access-Control-Allow-Origin': '*'})

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    # Development only! Reloads server on file change.
    init_db()
    app.debug = True
    app.run()
