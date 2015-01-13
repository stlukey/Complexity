#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: fab/pip.py
    ~~~~~~~~~~~~~~~~~~~~~~
    
    Fabric file for managing Complexity's functions for pip.

    :copyright: (c) 2014 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""

from fabric.api import task, local
from fabric.colors import *

from . import REQS

@task
def update_reqs():
    print magenta("Updating the requirements...")

    local('pip freeze > %s' % REQS)

    print green("Done updating requirements!")

@task
def install_reqs():
    print magenta("Starting requirements install...")
    install('-r %s' % REQS, update=False)
    print green("Installed all of the requirements!")

@task
def install(package, update=True):
    print magenta("Installing %s.." % package)
    local('pip install %s' % package)

    if update:
        update_reqs()

    print green("Finished install!")

