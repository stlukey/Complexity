#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: Flask app
    ~~~~~~~~~~~~~~~~~~~~~
    
    Contains the flask app.

    :copyright: (c) 2014 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""


import os

from flask import Flask, render_template
from flask.ext import shelve, assets

from quiz import quiz

# Configuration
SHELVE_FILENAME = 'complexity.bin'

# Set up Flask app instance.
app = Flask(__name__)
app.config.from_object(__name__)

# Set up the shelve
shelve.init_app(app)


# Set up flask Assets
env = assets.Environment(app)

# Tell flask-assets where to look for our coffeescript and sass files.
ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')

env.load_path = [
    os.path.join(ASSETS_PATH, path)
        for path in ['less', 'coffee', 'bower_components']
]

env.register(
    'js_all',
    assets.Bundle(
        'jquery/dist/jquery.min.js',
        'bootstrap/dist/js/bootstrap.min.js',
        assets.Bundle(
            'all.coffee',
            filters=['coffeescript']
        ),
        output='all.js'
    )
)

env.register(
    'css_all',
    assets.Bundle(
        'all.less',
        filters='less',
        output='all.css',
        depends=['**/*.less']
    )
)

@app.route("/")
def index():
    return render_template('index.html')

app.register_blueprint(quiz, url_prefix="/quiz")

