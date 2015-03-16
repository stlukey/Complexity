#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: utils.py
    ~~~~~~~~~~~~~~~~~~~~

    General utilities.

"""

from flask import g
from custom import shelve


def get_shelve(flag="c"):
    """
    Get shelve and cache for the request.

    :param flag: Flag parmeter for `shelve.get_shelve`.
    """
    if hasattr(g, 'shelve'):
        f, s = g.shelve
        if flag == f:
            return s
        s.close()

    s = shelve.get_shelve(flag)
    g.shelve = (flag, s)

    return s

