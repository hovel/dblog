#!/usr/bin/env python

from distutils.core import setup, find_packages

setup(
name = 'dblog',
version = '1.1',
packages = find_packages(),
include_package_data = True,
package_data = {'dblog': [
    'templatetags/*',
    'urls/*',
    'templates/*/*',
    'fixtures/*',
    'locale/*/*',
    'migrations/*']},
)