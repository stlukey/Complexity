#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: errors.py
    ~~~~~~~~~~~~~~~~~~~~~

    Contains custom exceptions.

    Copyright: (c) 2014 Luke Southam <luke@devthe.com>.
    License: New BSD, see LICENSE for more details.
"""


class BaseError(Exception):
    def __init__(self, status_code, message, error=None):
        Exception.__init__(self)
        self.status_code = status_code
        self._message = message
        if error is not None:
            self._error = error

    @property
    def error(self):
        if not hasattr(self, '_error'):
            self._error = self.__class__.__name__
        return self._error

    def to_dict(self):
        return {
            'status_code': self.status_code,
            'error': self.error,
            'message': self.message
        }

    def to_text(self):
        return "{}, {}: {}".format(
            self.status_code,
            self.error,
            self.message
        )

    def to_html(self):
        return "<h1>{}, {}:</h1> <p>{}</p>".format(
            self.status_code,
            self.error,
            self.message
        )


class BadRequestError(BaseError):
    status_code = 400

    def __init__(self, message):
        self.message = message