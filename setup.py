#!/usr/bin/env python

from distutils.core import setup

setup(
name = 'dblog',
version = '1.0',
package_dir = {'dblog': 'dblog'},
package_data = {'': [
    'templatetags/*',
    'urls/*',
    'templates/*/*',
    'fixtures/*',
    'locale/*/*',
    'migrations/*']},
packages = ['dblog'],
)