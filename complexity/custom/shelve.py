#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: custom/shelve.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Mimics the `flask-shelves` module but adds more advanced
    deserialization through the `dill` package instead of `pickle`
    allowing almost any type of object to be stored.

    :copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""

import sys
from flask.ext import shelve

# This module === flask-shelves
sys.modules[__name__] = shelve

# Now we can make changes as if we just copied the contents of
# `flask-shelves` into this file but without the duplication of code.
import shelve
import dill

# Use `dill` instead of `pickle`.
shelve.Pickler = dill.Pickler
shelve.Unpickler = dill.Unpickler
