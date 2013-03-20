from flask import Flask, jsonify
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/json/example")
def get_json():
    return jsonify(name='toast',
                   count=1)

if __name__ == "__main__":
    # Development only! Reloads server on file change.
    app.debug = True
    app.run()
