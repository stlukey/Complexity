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
import base64
import uuid

from fabric.api import task, local
from fabric.colors import *

from fab import pip

from complexity import create_app
from complexity import command_line
from complexity._secrets import __doc__ as secrets_doc

@task
def run():
    command_line.run()

@task
def debug():
    command_line.debug()

@task
def pyclean():
    print magenta("Cleaning python cache...")
    local('find . -type f -name "*.py[co]" -delete')
    local('find . -type d -name "__pycache__" -delete')
    print green("Done cleaning python cache files!")

@task
def clean():
    clean_storage()
    print magenta("Cleaning all temporary files...")
    pyclean()
    local('find . -type d -name ".*.swp" -delete')

    print green("Done cleaning temporary files!")

@task
def create_secrets():
    cookie_secret = base64.b64encode(
        uuid.uuid4().bytes + uuid.uuid4().bytes
    )
        
    with open('complexity/secrets.py', 'w') as f:
        f.write("""#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
\"\"\"
{}
\"\"\"
# NOTE: This file was automatically generated.
COOKIE_SECRET='{}'
""".format(secrets_doc, cookie_secret))

@task
def clean_storage():
    print magenta("Cleaning storage...")

    local('rm -f complexity.bin')
    local('rm -f complexity.bin.lock')

    print green("Done cleaning storage.")
