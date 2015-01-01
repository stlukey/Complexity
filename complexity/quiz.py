#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: quiz.py
    ~~~~~~~~~~~~~~~~~~~
    
    Contains the quiz blueprint.

    Copyright: (c) 2014 Luke Southam <luke@devthe.com>.
    License: New BSD, see LICENSE for more details.
"""

from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask.ext import shelve

from quizes import quizes, quizes_rev, quizes_path, load_quiz, register_assets

quiz = Blueprint('quiz', __name__, template_folder='templates/quizes')

@quiz.route("/")
def choose():
    """
    Get user to choose which quiz.

    Returns a HTML page with a form, then redircts them to the
    correct quiz's page once the form is submited.
    """

    # Ask user which quiz.
    if 'quiz' not in request.args:
        return render_template('new.html', quizes=quizes)

    # Redirect quiz request to the correct page.
    return redirect(
        url_for(
            'quiz.attempt',
            quiz_module=request.args['quiz']
        )
    )

@quiz.route("/<quiz_module>")
def attempt(quiz_module):
    """
    Attempt the quiz.

    Returns the HTML page for the quiz.

    Args:
        quiz_module (str): The name of the module in the `quizes`
                           package where the `Quiz` class exists.

    Raises:
        abort(404): When the requested `quiz_module` does not exist.
    """

    # Check the quiz exists.
    if quiz_module not in quizes.values():
        raise abort(404)

    return render_template(
        "%s.html" % quiz_module,
        quiz_name=quizes_rev[quiz_module],
        quiz_module=quiz_module
    )

@quiz.route("/<quiz_module>/new")
def new(quiz_module):
    """
    Create a new quiz instance.

    Used by client side code to get a quiz instance.

    Args:
        quiz_module (str): The name of the module in the `quizes`
                           package where the `Quiz` class exists.

    Returns:
        str: The Quiz instance's ID.

    Raises:
        abort(404): When the requested `quiz_module` does not exist.
    """

    # Check the quiz exists.
    if quiz_module not in quizes.values():
        raise abort(404)
    
    Quiz = load_quiz(quiz_module) 
    
    return Quiz.create_new(shelve.get_shelve('c'))

