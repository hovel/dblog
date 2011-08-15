#!/usr/bin/env python

from distutils.core import setup

setup(
name = 'dblog',
version = '1.0',
packages = ['dblog'],
package_dir={'dblog': 'dblog'},
package_data = {'dblog': [
    'templatetags/*',
    'urls/*',
    'templates/*/*',
    'fixtures/*',
    'locale/*/*',
    'migrations/*']},
)
