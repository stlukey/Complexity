
import sys
from flask.ext import shelve
import dill

shelve.shelve.Pickler = dill.Pickler
shelve.shelve.Unpickler = dill.Unpickler

sys.modules[__name__] = shelve

