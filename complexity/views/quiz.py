#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: views/quiz.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Contains the quiz blueprint.

    :copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""
from functools import wraps
import bisect

from flask import (Blueprint, render_template, request, redirect,
                   url_for, abort, g, make_response, jsonify,
                   Response, current_app)

from ..cookie import Cookie
from ..utils import get_shelve
from ..quizzes import quizzes, quizzes_rev, load_quiz, BaseQuiz
from ..errors import BadRequestError

COOKIE_QUIZ = 'quiz'

quiz_bp = Blueprint(
    'quiz', __name__,
    template_folder='../templates/quizzes'
)


def quiz_cookie_manage(response):
    """
    Manages quiz instances set at g.quiz_id

    Used by controllers with @after_request.
    """
    quiz_req = Cookie(request.cookies.get(COOKIE_QUIZ), False).data

    quiz_resp = None
    if hasattr(g, 'quiz_id'):
        quiz_resp = g.quiz_id
    
    # No more instances.
    if quiz_resp is None:
        if quiz_req is None:
            # There wasn't any instances. Still aren't.
            return
        
        # The instance did not get renewed.
        try:
            BaseQuiz.remove_instance(get_shelve('c'), quiz_req)
        except KeyError:
            pass
        return response.set_cookie(COOKIE_QUIZ, '', expires=0)
    
    # Still an instance, but not the same as before (may not have
    # been one before).
    if quiz_resp != quiz_req:
        if quiz_req is not None:
            # Old instance has been replaced.
            try:
                BaseQuiz.remove_instance(get_shelve('c'), quiz_req)
            except KeyError:
                pass

        # A new instance has been created.
        return response.set_cookie(
            COOKIE_QUIZ, Cookie(quiz_resp).value
        )
    
    # If no return by now, nothing has changed.


def quiz_cookie(func):
    """
    Runs quiz_cookie_manage on response object after request.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)

        # Ensure the response is a response object.
        if not isinstance(response, Response):
            response = make_response(response)

        quiz_cookie_manage(response)
        return response
    return wrapper


@quiz_bp.route("/")
@quiz_cookie
def choose():
    """
    Get user to choose which quiz.

    :returns: An HTML page with a form, then redirects them to the
              correct quiz's page once the form is submitted.
    """
    # Ask user which quiz.
    if 'quiz' not in request.args:
        return render_template('new.html', quizzes=quizzes)

    # Redirect quiz request to the correct page.
    return redirect(
        url_for(
            'quiz.attempt',
            quiz_module=request.args['quiz']
        )
    )


@quiz_bp.route("/<quiz_module>")
@quiz_cookie
def attempt(quiz_module):
    """
    Attempt the quiz.

    :param quiz_module: The name of the module in the `quizzes`
                        package where the `Quiz` class exists.

    :returns the HTML page for the quiz.

    :raises abort(404): When the requested `quiz_module` does not
                        exist.
    """

    # Check that the quiz exists.
    if quiz_module not in quizzes.values():
        raise abort(404)

    # Build template vars.
    template_vars = {}
    template_vars['quiz_name'] = quizzes_rev[quiz_module]
    template_vars['quiz_module'] = quiz_module
    template_vars['SCRIPT_QUIZ_URLS'] = {
        # Create dictionary of endpoints for client side scripts.
        rule.endpoint[len('quiz._'):]:
            url_for(rule.endpoint, quiz_module=quiz_module)
            for rule in current_app.url_map.iter_rules()
            if rule.endpoint.startswith('quiz._')
    }

    return render_template("%s.html" % quiz_module, **template_vars)

# NOTE: Endpoints used by client side scripts begin with a '_'


@quiz_bp.route("/<quiz_module>/_new")
@quiz_cookie
def _new(quiz_module):
    """
    Create a new quiz instance.

    Used by client side code to get a quiz instance.

    :param quiz_module: The name of the module in the `quizzes`
                        package where the `Quiz` class exists.

    :returns: The Quiz instance's ID.

    :raises abort(404): The requested `quiz_module` does not exist.
    """

    # Check the quiz exists.
    if quiz_module not in quizzes.values():
        raise abort(404)
    
    Quiz = load_quiz(quiz_module) 
    
    g.quiz_id = Quiz.create_new(get_shelve())
    
    return jsonify(dict(ID=g.quiz_id))


@quiz_bp.route("/<quiz_module>/_next", methods=['GET', 'POST'])
@quiz_cookie
def _next(quiz_module):
    """
    Answer/Ask next question.

    :param quiz_module: The name of the module in the `quizzes`
                        package where the `Quiz` class exists.

    :returns: The quiz's response.

    :raises BadRequestError:
    :raises abort(404): The requested `quiz_module` does not exist.
    """
    # Check the quiz exists.
    if quiz_module not in quizzes.values():
        raise abort(404)

    quiz_id = Cookie(request.cookies.get(COOKIE_QUIZ), False).data
    if quiz_id is None:
        raise BadRequestError("No Quiz ID!")

    json = None
    if request.method == 'POST':
        json = request.get_json()

        if not isinstance(json, dict):
            raise BadRequestError("Expected json object.")

    quiz = load_quiz(quiz_module).get_instance(get_shelve(), quiz_id)
    resp = jsonify(quiz.next(json))

    g.quiz_id = quiz.save(get_shelve())
    return resp

@quiz_bp.route("/<quiz_module>/finish", methods=['POST'])
@quiz_cookie
def _finish(quiz_module):
    """
    Finish quiz.
    """
    # Check the quiz exists.
    if quiz_module not in quizzes.values():
        raise abort(404)

    quiz_id = Cookie(request.cookies.get(COOKIE_QUIZ), False).data
    if quiz_id is None:
        raise BadRequestError("No Quiz ID!")

    quiz = load_quiz(quiz_module).get_instance(get_shelve(), quiz_id)
    if not quiz.ended:
        raise BadRequestError("Quiz not ended!")

    shelve = get_shelve()


    name = request.form.get('name', None)
    if name:
        record = quiz.finish(name)
        quiz_module = str(quiz_module)
        records = shelve.get(quiz_module, [])

        records.append(record)
        records.sort(reverse=True)
        shelve[quiz_module] = records

    quiz.remove(shelve)

    return redirect(url_for('root.index'))


