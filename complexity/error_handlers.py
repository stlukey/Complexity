#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: error_handlers.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Handlers for custom exceptions.

"""

from flask import jsonify, request, make_response

from errors import BaseError

# A place to store error handlers before they get registered.
errorhandlers = {}

def errorhandler(error):
    """
    Add error handler.

    :param error: The error class.
    """
    def wrapper(func):
        errorhandlers[error] = func
        return func
    return wrapper

def register_errorhandlers(app):
    """
    Register error handlers.

    :param app: The application's instance.
    """
    for error, handler in errorhandlers.iteritems():
        app.errorhandler(error)(handler)

@errorhandler(BaseError)
def handle_base_error(error):
    """
    Renders response content for when a custom exception is made.

    :param error: The error instance.
    """
    # If the endpoint starts with '_', respond in JSON not HTML.
    endpoint = request.endpoint.split('.')[-1]
    response = make_response(jsonify(error.to_dict())
                             if endpoint.startswith('_')
                             else error.to_html())

    response.status_code = error.status_code
    return response


