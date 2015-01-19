#!/usr/bin/assets python2
# -*- coding: UTF-8 -*-
"""
    Complexity: Flask views.
    ~~~~~~~~~~~~~~~~~~~~~~~~
    
    Contains the views and registers blueprints.

    :copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""
from flask import render_template

from .. import app
from .quiz import quiz_bp
from .records import records_bp

# Register error handlers.
from .. import error_handlers


@app.route("/")
def index():
    """
    The index page.
    Just welcomes the user and asks them to start a quiz. 
    """
    return render_template('index.html')

# Register blueprints.
app.register_blueprint(quiz_bp, url_prefix="/quiz")
app.register_blueprint(records_bp, url_prefix="/records")
