#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: Flask app
    ~~~~~~~~~~~~~~~~~~~~~
    
    Sets up the flask app.

    :copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""

import os
from importlib import import_module

from flask import Flask
from .custom import shelve
from .custom.assets import Bundle, Environment

from .quizzes import quiz_modules

# NOTE: Ideally either a JSON file or a file containing a pickled
#       Python dictionary would be used for storage as the storage
#       required is not significant enough for a database. However
#       the problem is multiple users could access the file at
#       the same time and some may need to write data at the same
#       time too. Python has a built-in module called 'shelves'
#       that builds on top of the 'pickle' module allowing for a
#       layer of abstraction, eliminating the need to manually write
#       the pickled data (binary data that represents python objects)
#       to the file. 'flask-shelves' is a reimplementation of the
#       built-in 'shelves' module for use with the Flask web
#       framework and provides a locking mechanism over the pickled
#       data file. Hence, this is why it is used for storage.

# ~~~~ Configuration ~~~~

# Data filename.
SHELVE_FILENAME = 'complexity.bin'
SHELVE_PROTOCOL = 1

# Assets.
ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')

# ~~~~~~~~~~~~~~~~~~~~~~~

def create_app(**config):
    """
    Creates the application object.
    
    This is moved into a function, instead of creating the object at
    import time, so that multiple instances can be created. This
    is mainly needed for testing.
    """

    # Flask app instance.
    app = Flask(__name__)
    app.config.from_object(__name__)

    # Add additional config.
    app.config.update(config) 

    # The shelve.
    shelve.init_app(app)

    # Flask Assets.
    assets = Environment(app)
    setup_assets(assets)
    
    # Register blueprints and error handlers.
    import_module('.views', package=__name__).register_blueprints(app)
    import_module('.error_handlers', package=__name__).register_errorhandlers(app)

    return app

def setup_assets(assets):
    """
    Sets up assets (client-side scripts and styling). 
    """

    # Define paths to look in for files.
    assets.load_path = [
        os.path.join(ASSETS_PATH, path)
        for path in ['less', 'coffee', 'bower_components']
    ]

    # Register all javascript files.
    assets.register(
        'js_all',
        Bundle(
            'jquery/dist/jquery.min.js',
            'jquery-color/jquery.color.js',
            'bootstrap/dist/js/bootstrap.min.js',
            'katex/katex.js',
            output='all.js'
        )
    )

    # Register all styling.
    assets.register(
        'css_all',
        Bundle(
            'all.less',
            'katex/static/katex.less',
            filters='less',
            output='all.css',
            depends=['**/*.less']
        )
    )
    
    # Register CoffeeScript files for each quiz.
    for module in quiz_modules:
        assets.register(
            'quiz-' + module,
            Bundle(
                Bundle(
                    'quizzes/{}.coffee'.format(module),
                    filters=['coffeescript']
                ),
                output='quiz-{}.js'.format(module)
            )
        )

