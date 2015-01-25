#!/usr/bin/assets python2
# -*- coding: UTF-8 -*-
"""
    Complexity: views/root.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Contains the root blueprints.

    :copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""
from flask import Blueprint, render_template

root_bp = Blueprint(
    'root', __name__,
    template_folder='../templates'
)

@root_bp.route("/")
def index():
    """
    The index page.
    Just welcomes the user and asks them to start a quiz. 
    """
    return render_template('index.html')

