from flask import Flask, send_file

from model import gen_plot

app = Flask(__name__)


@app.route("/")
def images():
    buffer = gen_plot()
    return send_file(buffer, mimetype='image/png')
