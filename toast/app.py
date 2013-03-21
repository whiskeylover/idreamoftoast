from flask import Flask, jsonify
from flask import render_template
import urllib2
import json

app = Flask(__name__)

#@app.route("/")
#def hello():
#    return render_template('index.html')
#
#@app.route("/dream/<dream>")
#def dream(dream):
#    return render_template('dream.html', my_dream=dream)
#
#

@app.route("/dream/define/<term>")
def get_urbandictionary(term):
    response = urllib2.urlopen('http://api.urbandictionary.com/v0/define?term=' + term)
    html = response.read()
    
    j = json.loads(html)
    return j['list'][0]['definition']

@app.route("/dreams/top")
def get_json():
    return jsonify(top_dreams=
                   [{dream:d1,count:100},
                    {dream:d2,count:80},
                    {dream:d3,count:60},
                    {dream:d4,count:40},
                    {dream:d5,count:20}
                   ]
                  )

@app.route("/dreams/recent")
def get_json():
    return jsonify(recent_dreams=
                   [{dream:d1,count:100},
                    {dream:d2,count:80},
                    {dream:d3,count:60},
                    {dream:d4,count:40},
                    {dream:d5,count:20}
                   ]
                  )


if __name__ == "__main__":
    # Development only! Reloads server on file change.
    app.debug = True
    app.run()
