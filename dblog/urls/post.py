from django.conf.urls import url
from django.views.generic import TemplateView

from dblog.feeds import LatestPostsFeed
from dblog.views import *

urlpatterns = [
    url(r'^$', PostList.as_view(), None, 'promoted'),
    url(r'^feed/$', LatestPostsFeed(), None, 'feed'),
    url(r'^create/$', PostCreate.as_view(), None, 'create'),
    url(r'^(?P<pk>\d+)/$', PostDetail.as_view(), None, 'detail'),
    url(r'^(?P<pk>\d+)/update/$', PostUpdate.as_view(), None, 'update'),
    url(r'^(?P<pk>\d+)/delete/$', PostDelete.as_view(), None, 'delete'),
    url(r'^(?P<pk>\d+)/manage/$', PostManage.as_view(), None, 'manage'),
    url(r'^tags/$', TemplateView.as_view(template_name='dblog/tags.html'), None, 'tags'),
    url(r'^tags/(?P<tag>[^/]+)/$', PostTaggedList.as_view(), None, 'tagged'),
]
