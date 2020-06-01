from flask import Flask, send_file, render_template

from model import gen_plot

app = Flask(__name__)

app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')
@app.route("/img/covr")
def images():
    buffer = gen_plot()
    return send_file(buffer, mimetype='image/svg+xml')

@app.route("/")
def main():
    return render_template('main.pug')