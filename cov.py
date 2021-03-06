from flask import Flask, send_file, render_template
from flask_caching import Cache

from model import gen_plot

cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)

cache.init_app(app)

app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')


@app.route("/img/covr")
@cache.cached(timeout=60 * 60)
def images():
    buffer = gen_plot()
    return send_file(buffer, mimetype='image/svg+xml')


@app.route("/")
def main():
    return render_template('main.pug')
