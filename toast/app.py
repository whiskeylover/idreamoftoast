from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/json/example")
def get_json():
    return jsonify(name='toast',
                   count=1)

if __name__ == "__main__":
    # Development only! Reloads server on file change.
    app.debug = True
    app.run()
