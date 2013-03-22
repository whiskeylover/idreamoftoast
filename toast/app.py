from flask import Flask, jsonify
from flask import render_template
import urllib2
import json

app = Flask(__name__)

FAKE_DATA = [{'name':'toast',
              'count':100},
             {'name':'pizza',
              'count':80},
             {'name':'bread',
              'count':60},
             {'name':'butter',
              'count':40},
             {'name':'beer',
              'count':20}]

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
    
    #return 'http://farm' + j['photos']['photo'][0]['farm'] + \
    #    '.staticflickr.com/' + j['photos']['photo'][0]['server'] + \
    #    '/' + j['photos']['photo'][0]['id'] + \
    #    '_' + j['photos']['photo'][0]['secret'] + \
    #    '_z.jpg'




@app.route("/dreams/top")
def top_dreams():
    return jsonify(data=FAKE_DATA)

@app.route("/dreams/recent")
def recent_dreams():
    return jsonify(data=FAKE_DATA)

if __name__ == "__main__":
    # Development only! Reloads server on file change.
    app.debug = True
    app.run()
