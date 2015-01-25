#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: fabfile.py
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""

from complexity import create_app

def run(debug=False):
    app = create_app()
    app.run(debug=debug)

def debug():
    run(True)

if __name__ == '__main__':
    run()

