__author__ = 'zeus'
from django.conf import settings
from markdown import markdown

DBLOG_BODY_RENDER = getattr(settings, 'DBLOG_BODY_RENDER', lambda body: markdown(body, safe_mode='remove'))
DBLOG_TEMPLATE = getattr(settings, 'DBLOG_TEMPLATE', 'base.html')