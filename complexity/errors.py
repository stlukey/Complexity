#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: errors.py
    ~~~~~~~~~~~~~~~~~~~~~

    Contains custom exceptions.

    Copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    License: New BSD, see LICENSE for more details.
"""


class BaseError(Exception):
    """
    The base for all custom error classes to inherit from.
    """
    def __init__(self, status_code, message, error=None):
        """
        :param status_code: HTTP status code.
        :param message: A little description of the error.
        :param error: A name of the error's type.
        """
        Exception.__init__(self)
        self.status_code = status_code
        self._message = message
        if error is not None:
            self._error = error

    @property
    def error(self):
        """
        Return the error name if provided or just the error's class
        name.
        """
        if not hasattr(self, '_error'):
            self._error = self.__class__.__name__
        return self._error

    def to_dict(self):
        """
        Render error as dictionary.
        (useful for API endpoints where it can be converted to JSON)
        """
        return {
            'status_code': self.status_code,
            'error': self.error,
            'message': self.message
        }

    def to_text(self):
        """
        Render text error message.
        """
        return "{}, {}: {}".format(
            self.status_code,
            self.error,
            self.message
        )

    def to_html(self):
        """
        Render HTML error message.
        """
        return "<h1>{}, {}</h1> <p>{}</p>".format(
            self.status_code,
            self.error,
            self.message
        )


class BadRequestError(BaseError):
    """
    Error for when an invalid request is made.
    """
    status_code = 400

    def __init__(self, message):
        """
        :param message: A little message describing why, exactly,
                        the request was wrong.
        """
        self.message = message