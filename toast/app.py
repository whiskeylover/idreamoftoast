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
