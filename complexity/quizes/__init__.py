#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: quizes/__init__.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""

import os
from pkgutil import iter_modules

import uuid

# Get the quizes package's path.
quizes_path = os.path.dirname(__file__)

# Find all quiz modules.
quiz_modules = [module for _, module, _ in iter_modules([quizes_path])]

# Create name (replace '_' with spaces and make title case).
quiz_names = [module.replace('_', ' ').title() for module in quiz_modules]

# Generate dictionary of quizes and there names.
quizes = {name:module for name in quiz_names for module in quiz_modules}

# For reverse lookup.
quizes_rev = {v: k for k, v in quizes.items()}


class BaseQuiz(object):
    @classmethod
    def create_new(cls, shelves):
        return cls().save(shelves)

    @staticmethod
    def get(shelves, id_):
        return shelves[id_]

    def id(self, shelves):
        if hasattr(self, '_id'):
            return self._id
        
        new_id = "quiz-{}".format(str(uuid.uuid4()))

        # If ID already used just generate another.
        if new_id in shelves:
            return self.id(shelves)

        # Claim the ID.
        shelves[new_id] = None
        
        # Save it for next time.
        self._id = new_id

        return new_id


    def save(self, shelves):
        shelves[self.id(shelves)] = self
        return self.id(shelves)
        
        

