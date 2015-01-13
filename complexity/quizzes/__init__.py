#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: quizzes/__init__.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""

import os
import uuid
from pkgutil import iter_modules
from .. import Bundle

SHELVE_INSTANCE_PREFIX = 'quiz-'

# Get the quizzes package's path.
quizzes_path = os.path.dirname(__file__)

# Find all quiz modules.
quiz_modules = [
    module for _, module, _ in iter_modules([quizzes_path])
]

# Create name (replace '_' with spaces and make title case).
quiz_names = [
    module.replace('_', ' ').title() for module in quiz_modules
]

# Generate dictionary of quizzes and there names.
quizzes = {
    name:module
        for name in quiz_names
            for module in quiz_modules
}

# For reverse lookup.
quizzes_rev = {v: k for k, v in quizzes.items()}

def register_assets(assets):
    """
    Create and register assets for every quiz.
    (cant relative import assets?)

    :param assets: Flask-Assets Environment.
    """
    for module in quiz_modules:
        assets.register(
            'quiz-' + module,
            Bundle(
                Bundle(
                    'quizzes/{}.coffee'.format(module),
                    filters=['coffeescript']
                ),
                output='quiz-{}.js'.format(module)
            )
        )

def load_quiz(quiz_module):
    """
    Load Quiz class for given module.
    
    :param quiz_module: Name of module that contains `Quiz` class
                        in the package `quizzes`.
    :type quiz_module: str

    :returns: The `Quiz` class from `quiz_module`.
    """

    # TODO: Load dynamicallly based on `quiz_modulus` once more than
    #       one quiz exists.
    from the_modulus import Quiz

    return Quiz

class BaseQuiz(object):
    """
    Base Quiz object that all Quiz objects MUST inherit from.
    """

    @classmethod
    def create_new(cls, shelve):
        """
        Create new instance of `cls` and save in shelve.

        :param shelve: The open shelve (file) from flask-shelves.

        :returns: The Quiz instance's ID.
        """
        return cls().save(shelve)

    @staticmethod
    def get_instance(shelve, id_):
        """
        Get instance from the shelve file.

        :param shelve: The open shelve (file) from flask-shelves.
        :param id_: The Quiz instance's ID.

        :returns: Quiz instance.
        """
        return shelve[SHELVE_INSTANCE_PREFIX + str(id_)]

    @classmethod
    def remove_instance(cls, shelve, id_):
        """
        Remove instance from shelve file.

        :param shelve: The open shelve (file) from flask-shelve.
        :param id_: The Quiz instance's ID.
        """
        cls.get_instance(shelve, id_).remove(shelve)

    def id(self, shelve):
        """
        Find or create and claim ID for instance.

        :param shelve: The open shelve (file) from flask-shelve.

        :returns: The Quiz instance's ID.
        """

        if hasattr(self, '_id'):
            return self._id
        
        new_id = str(uuid.uuid4())
        full_id = SHELVE_INSTANCE_PREFIX + new_id

        # If ID already used just generate another.
        if full_id in shelve:
            return self.id(shelve)

        # Claim the ID.
        shelve[full_id] = None
        
        # Save it for next time.
        self._id = new_id

        return new_id

    def save(self, shelve):
        """
        Save instance to shelve file.

        :param shelve: The open shelve (file) from flask-shelve.

        :returns: The Quiz instance's ID.
        """
        id_ = self.id(shelve)
        shelve[SHELVE_INSTANCE_PREFIX + id_] = self
        return id_

    def remove(self, shelve):
        """
        Remove instance from shelve file.

        :param shelve: The open shelve (file) from flask-shelve.
        """
        id_ = self.id(shelve)
        del shelve[SHELVE_INSTANCE_PREFIX + id_]

