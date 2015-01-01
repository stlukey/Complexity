#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: quiz.py
    ~~~~~~~~~~~~~~~~~~~
    
    Contains the quiz blueprint.

    :copyright: (c) 2014 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""

from flask import Blueprint, render_template, request, redirect, url_for, abort

from quizes import quizes, quizes_rev, quizes_path

from flask.ext import shelve


quiz = Blueprint('quiz', __name__, template_folder='templates/quizes')



@quiz.route("/<quiz_module>")
def attempt(quiz_module):
    if quiz_module not in quizes.values():
        raise abort(404)

    return render_template(
        "%s.html" % quiz_module,
        quiz_name=quizes_rev[quiz_module]
    )

@quiz.route("/<quiz_module>/new")
def new(quiz_module):
    if quiz_module not in quizes.values():
        raise abort(404)
    
    from quizes.the_modulus import Quiz
    
    return Quiz.create_new(shelve.get_shelve('c'))

@quiz.route("/")
def choose():
    if 'quiz' in request.args:
        return redirect(
            url_for(
                'quiz.attempt',
                quiz_module=request.args['quiz']
            )
        )

    return render_template('new.html', quizes=quizes)


