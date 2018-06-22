from flask import Flask, render_template, jsonify
import json


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('g61.html')


@app.route("/getData")
def get_data():
    with open("./data/nodes.json", "r") as f:
        data = json.load(f)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)