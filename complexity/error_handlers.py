#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: error_handlers.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Handlers for custom exceptions.

    Copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    License: New BSD, see LICENSE for more details.
"""

from flask import jsonify, request, make_response

from errors import BaseError

# A place to store error handlers before they get registered.
errorhandlers = {}

def errorhandler(error):
    """
    Add error handler.
    """
    def wrapper(func):
        errorhandlers[error] = func
        return func
    return wrapper

def register_errorhandlers(app):
    """
    Register error handlers.
    """
    for error, handler in errorhandlers.iteritems():
        app.errorhandler(error)(handler)

@errorhandler(BaseError)
def handle_base_error(error):
    """
    Renders response content for when a custom exception is made.
    """
    # If the endpoint starts with '_', respond in JSON not HTML.
    endpoint = request.endpoint.split('.')[-1]
    response = make_response(jsonify(error.to_dict())
                             if endpoint.startswith('_')
                             else error.to_html())

    response.status_code = error.status_code
    return response


