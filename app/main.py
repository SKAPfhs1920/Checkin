from flask import Flask, url_for, jsonify
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

import api
api.register(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
import model


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
