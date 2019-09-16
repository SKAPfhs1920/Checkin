from flask import Flask, url_for, jsonify
app = Flask(__name__)

import api

api.register(app)

@app.route("/hello")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route("/site-map")
def site_map():
    links = {}
    for rule in app.url_map.iter_rules():
        links[rule.rule] = rule.endpoint

    return jsonify(links)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
