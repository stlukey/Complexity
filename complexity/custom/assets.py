import sys
from flask.ext import assets as assets_
sys.modules[__name__] = assets_

from webassets.filter import register_filter, Filter
from webassets.filter.coffeescript import CoffeeScript


class CoffeeScriptNotBare(Filter):
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
