#!/usr/bin/assets python2
# -*- coding: UTF-8 -*-
"""
    Complexity: Flask app
    ~~~~~~~~~~~~~~~~~~~~~
    
    Contains the flask app.

    Copyright: (c) 2014 Luke Southam <luke@devthe.com>.
    License: New BSD, see LICENSE for more details.
"""

import os

from flask import Flask, render_template
from flask.ext import shelve
from flask.ext.assets import Bundle, Environment

from quizes import register_assets as register_quizes_assets

from utils import get_shelve

# NOTE: Idealy either a JSON file or a file containing a pickled
#       Python dictionary would be used for storage as the storage
#       required is not significant enough for a database. However
#       the problem is multiple users could access the file at
#       the same time and some may need to write data at the same
#       time too. Python has a built-in module called 'shelves'
#       that builds ontop of the 'pickle' module allowing for a
#       layer of abstraction, eliminating the need to manually write
#       the pickled data to the file. 'flask-shelves' is a
#       reimplementaion of the built-in 'shelves' module for use
#       with the Flask web framework and provides a locking
#       mechanism over the pickled data file. Hence, this is why it
#       is used for storage.

####### Configuration #######

# Data filename.
SHELVE_FILENAME = 'complexity.bin'

# Assets directory.
ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')

########### Setup ###########

# Flask app instance.
app = Flask(__name__)
app.config.from_object(__name__)

# The shelve.
shelve.init_app(app)

# Flask Assets.
assets = Environment(app)

########## Assets ###########

assets.load_path = [
    os.path.join(ASSETS_PATH, path)
        for path in ['less', 'coffee', 'bower_components']
]

assets.register(
    'js_all',
    Bundle(
        'jquery/dist/jquery.min.js',
        'bootstrap/dist/js/bootstrap.min.js',
        Bundle(
            'all.coffee',
            filters=['coffeescript']
        ),
        output='all.js'
    )
)

assets.register(
    'css_all',
    Bundle(
        'all.less',
        filters='less',
        output='all.css',
        depends=['**/*.less']
    )
)

register_quizes_assets(assets)

#############################

# Now every thing is set up load the views.

import views

