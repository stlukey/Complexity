#!/usr/bin/assets python2
# -*- coding: UTF-8 -*-
"""
    Complexity: Flask views.
    ~~~~~~~~~~~~~~~~~~~~~~~~
    
    Registers blueprints.

    :copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""
from .root import root_bp
from .quiz import quiz_bp
from .records import records_bp

def register_blueprints(app):
    """
    Register the applications blueprints.

    :param app: The Flask application object.
    """
    app.register_blueprint(root_bp)
    app.register_blueprint(quiz_bp, url_prefix="/quiz")
    app.register_blueprint(records_bp, url_prefix="/records")

