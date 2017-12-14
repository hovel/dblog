from django.conf.urls import url

from dblog.views import *

urlpatterns = [
    url(r'^$', BlogList.as_view(), None, 'list'),
    url(r'^(?P<pk>\d+)/$', BlogPostList.as_view(), None, 'detail'),
    url(r'^(?P<pk>\d+)/drafts/$', BlogPostDraftsList.as_view(), None, 'drafts'),
    url(r'^(?P<pk>\d+)/update/$', BlogUpdate.as_view(), None, 'update'),
]
