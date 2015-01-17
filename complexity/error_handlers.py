#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: error_handlers.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Handlers for custom exceptions.

    Copyright: (c) 2014 Luke Southam <luke@devthe.com>.
    License: New BSD, see LICENSE for more details.
"""

from flask import jsonify, request, make_response

from . import app
from errors import BadRequestError


@app.errorhandler(BadRequestError)
def handle_base_error(error):
    endpoint = request.endpoint.split('.')[-1]
    response = make_response(jsonify(error.to_dict())
                             if endpoint.startswith('_')
                             else error.to_html())
    response.status_code = error.status_code
    return response
