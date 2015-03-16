#!/usr/bin/assets python2
# -*- coding: UTF-8 -*-
"""
    Complexity: views/__init__.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Views for the application grouped by blueprint.

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

