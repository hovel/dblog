#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'

import defaults


def processor(request):
    context = {}
    for i in (
            'DBLOG_TEMPLATE',
    ):
        context[i] = getattr(defaults, i, None)
    return context
