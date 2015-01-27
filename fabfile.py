#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: fabfile.py
    ~~~~~~~~~~~~~~~~~~~~~~
    
    Fabric file for managing Complexity.

    :copyright: (c) 2015 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""
import os

from fabric.api import task, local
from fabric.colors import *

from fab import pip

from complexity import create_app
from complexity.command_line import run, debug

map(task, [run, debug])

@task
def pyclean():
    print magenta("Cleaning python cache...")
    local('find . -type f -name "*.py[co]" -delete')
    local('find . -type d -name "__pycache__" -delete')
    print green("Done cleaning python cache files!")

@task
def clean():
    print magenta("Cleaning all temporary files...")
    pyclean()
    local('find . -type d -name ".*.swp" -delete')

    local('rm complexity.bin.lock')

    print green("Done cleaning temporary files!")

@task
def clean_storage():
    print magenta("Cleaning storage...")

    local('rm -f complexity.bin')
    local('rm -f complexity.bin.lock')

    print green("Done cleaning storage.")
