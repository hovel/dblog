from django.conf.urls.defaults import *

from dblog.views import *

urlpatterns = patterns('',
    (r'^$', BlogList.as_view(), None, 'list'),
    (r'^(?P<pk>\d+)/$', BlogDetail.as_view(), None, 'detail'),
    (r'^(?P<pk>\d+)/update/$', BlogUpdate.as_view(), None, 'update'),
)

