from django.conf.urls.defaults import *

from dblog.views import *

urlpatterns = patterns('',
    (r'^$', BlogList.as_view(), None, 'list'),
    (r'^(?P<pk>\d+)/$', BlogPostList.as_view(), None, 'detail'),
    (r'^(?P<pk>\d+)/drafts/$', BlogPostDraftsList.as_view(), None, 'drafts'),
    (r'^(?P<pk>\d+)/update/$', BlogUpdate.as_view(), None, 'update'),
)

