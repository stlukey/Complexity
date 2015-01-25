from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import os
import io
import sys

import complexity

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')
requires = read('requirements.txt').splitlines()

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='complexity',
    version='0.0.1',
    url='http://github.com/o4dev/Complexity',
    license='New BSD',
    author='Luke Southam',
    tests_require=['pytest'],
    install_requires=requires,
    cmdclass={'test': PyTest},
    author_email='luke@devthe.com',
    description='Learn complex numbers, in a not so complex way!',
    long_description=long_description,
    packages=find_packages(exclude=['fab*', 'tests*']),
    include_package_data=True,
    platforms='any',
    test_suite='complexity.test',
    extras_require={
        'testing': ['pytest'],
    },
    package_data={
      'assets': 'complexity/assets/*',
      'templates': 'complexity/static/.gitignore'
    },
    entry_points = {
        'console_scripts': [
            'complexity-run = complexity.command_line:run',
            'complexity-debug = complexity.command_line:debug',
        ]
    }
)
