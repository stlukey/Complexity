#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: command_line.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Entry points for the application.

"""

from complexity import create_app

def run(debug=False):
    """
    Create an application instance and run it.

    :param debug: Debug option for `flask.Flask`.
    """
    app = create_app()
    app.run(debug=debug)

def debug():
    """
    Create an application instance for debugging and run it.
    """
    run(True)

# If this is run directly and not via an import.
if __name__ == '__main__':
    run()

