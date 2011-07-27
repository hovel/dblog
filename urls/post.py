from django.conf.urls.defaults import *

from dblog.views import *

urlpatterns = patterns('',
    (r'^create/$', PostCreate.as_view(), None, 'create'),
    (r'^(?P<pk>\d+)/$', PostDetail.as_view(), None, 'detail'),
    (r'^(?P<pk>\d+)/update/$', PostUpdate.as_view(), None, 'update'),
    (r'^(?P<pk>\d+)/delete/$', PostDelete.as_view(), None, 'delete'),
    (r'^(?P<pk>\d+)/promote/$', PostPromote.as_view(), None, 'promote'),
    (r'^(?P<pk>\d+)/demote/$', PostDemote.as_view(), None, 'demote'),
)

