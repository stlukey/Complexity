#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: quizes/__init__.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""

import os
import uuid
from pkgutil import iter_modules
from flask.ext.assets import Bundle

SHELVE_INSTANCE_PREFIX = 'quiz-'
COOKIE_INSTANCE_KEY = 'quiz'

# Get the quizes package's path.
quizes_path = os.path.dirname(__file__)

# Find all quiz modules.
quiz_modules = [
    module for _, module, _ in iter_modules([quizes_path])
]

# Create name (replace '_' with spaces and make title case).
quiz_names = [
    module.replace('_', ' ').title() for module in quiz_modules
]

# Generate dictionary of quizes and there names.
quizes = {
    name:module
        for name in quiz_names
            for module in quiz_modules
}

# For reverse lookup.
quizes_rev = {v: k for k, v in quizes.items()}

def register_assets(assets):
    """
    Create and register assets for every quiz.
    (cant relative import assets?)

    Args:
        assets (Environment): Flask-Assets Environment.
    """
    for module in quiz_modules:
        assets.register(
            'quiz-' + module,
            Bundle(
                Bundle(
                    'quizes/{}.coffee'.format(module),
                    filters=['coffeescript']
                ),
                output='quiz-{}.js'.format(module)
            )
        )

def load_quiz(quiz_module):
    """
    Load Quiz class for given module.
    
    Args:
        quiz_module (str): Name of module that contains `Quiz` class
                           in the package `quizes`.

    Returns:
        Quiz (BaseQuiz): The `Quiz` class from `quiz_module`.

    """

    # TODO: Load dynamicallly based on `quiz_modulus` once more than
    #       one quiz exists.
    from the_modulus import Quiz

    return Quiz

def delete_instance():
    pass

def add_instance(instance_id):
    pass

def get_instance():
    pass

class BaseQuiz(object):
    """
    Base Quiz object that all Quiz objects MUST inherit from.

    Attributes:
       _id (str): Private, access via `self.id` method.
    """

    @classmethod
    def create_new(cls, shelve):
        """
        Create new instance of `cls` and save in shelve.

        Args:
            cls (BaseQuiz): The Quiz class.
            shelve (Shelve): The open shelve (file) from flask-shelves. 

        Returns:
            str: The Quiz instance's ID.
        """
        return cls().save(shelve)

    @staticmethod
    def get_instance(shelve, id_):
        """
        Get instance from the shelve file.

        Args:
            shelve (Shelve): The open shelve (file) from flask-shelves.
            id_ (str): The Quiz instance's ID.

        Returns:
            quiz (BaseQuiz): Quiz instance.
        """
        return shelve[SHELVE_INSTANCE_PREFIX + id_]

    def id(self, shelve):
        """
        Find or create and claim ID for instance.

        Args:
            shelve (Shelve): The open shelve (file) from flask-shelve.

        Returns:
            str: The Quiz instance's ID.
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
        Save instance.

        Args:
            shelve (Shelve): The open shelve (file) from flask-shelve.

        Returns:
            str: The Quiz instance's ID.
        """
        id_ = self.id(shelve)
        shelve[SHELVE_INSTANCE_PREFIX + id_] = self
        return id_
        
