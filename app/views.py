from app import app

from flask import render_template, url_for, flash

@app.route('/')
@app.route('/index')
def index():
    nav = [
        {'href': url_for('index'), 'caption': 'Index'},
        ]
    flash("Velkommen til Alda")
    return render_template('index.j2', nav=nav, title="Forside")