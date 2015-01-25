#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: views/records.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Contains the records blueprint.

    :copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""

from flask import (Blueprint, redirect, url_for, request,
                   render_template)

from ..quizzes import quizzes, quizzes_rev
from ..utils import get_shelve

records_bp = Blueprint(
    'records', __name__,
    template_folder='../templates/records'
)

@records_bp.route('/')
def choose():
    """
    Get user to choose which quiz.

    :returns: An HTML page with a form, then redirects them to the
              correct quiz's record page once the form is submitted.
    """
    # Ask user which quiz.
    if 'quiz' not in request.args:
        return render_template('choose.html', quizzes=quizzes)

    # Redirect quiz request to the correct page.
    return redirect(
        url_for(
            'records.view',
            quiz_module=request.args['quiz']
        )
    )

@records_bp.route("/<quiz_module>")
def view(quiz_module):
    """
    View a quiz's records.

    :param quiz_module: The name of the module in the `quizzes`
                        package where the `Quiz` class exists.

    :returns the quiz's records page.

    :raises abort(404): When the requested `quiz_module` does not
                        exist.
    """

    # Check that the quiz exists.
    if quiz_module not in quizzes.values():
        raise abort(404)

    quiz_module = str(quiz_module)
    shelve = get_shelve()
    if quiz_module not in shelve:
        shelve[quiz_module] = []
    records = shelve[quiz_module]

    records_range = range(len(records))
    quiz_name = quizzes_rev[quiz_module]

    return render_template("view.html", **locals())
