
import sys
from flask.ext import shelve


sys.modules[__name__] = shelve

import shelve
import dill

# Use `dill` instead of `pickle`.
shelve.Pickler = dill.Pickler
shelve.Unpickler = dill.Unpickler


