#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: custom/assets.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Creates a new filter for CoffeeScript in `webassets`
    because `flask-assets` prevents `OPTIONS` being past to
    the filters in `webassets`.

    :copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""

import sys
from flask.ext import assets as assets_
sys.modules[__name__] = assets_

from webassets.filter import register_filter, Filter
from webassets.filter.coffeescript import CoffeeScript


class CoffeeScriptNotBare(Filter):
    """
    Adds default CoffeeScript behaviour to filter, adding a closure
    around the code ensuring other libraries don't interfere with it.
    """
    name = 'coffeescript'
    max_debug_level = None
    options = {
        'coffee_deprecated': (False, 'COFFEE_PATH'),
        'coffee_bin': ('binary', 'COFFEE_BIN'),
    }

    def output(self, *args, **kwargs):
        self.no_bare = True
        CoffeeScript.__dict__['output'](self, *args, **kwargs)

register_filter(CoffeeScriptNotBare)
