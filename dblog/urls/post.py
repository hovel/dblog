from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from dblog.feeds import LatestPostsFeed
from dblog.models import Post
from dblog.views import *

from tagging.views import tagged_object_list

urlpatterns = patterns('',
    (r'^$', PostList.as_view(), None, 'promoted'),
    (r'^feed/$', LatestPostsFeed(), None, 'feed' ),
    (r'^create/$', PostCreate.as_view(), None, 'create'),
    (r'^(?P<pk>\d+)/$', PostDetail.as_view(), None, 'detail'),
    (r'^(?P<pk>\d+)/update/$', PostUpdate.as_view(), None, 'update'),
    (r'^(?P<pk>\d+)/delete/$', PostDelete.as_view(), None, 'delete'),
    (r'^(?P<pk>\d+)/manage/$', PostManage.as_view(), None, 'manage'),
    (r'^tags/$', TemplateView.as_view(template_name='dblog/tags.html'), None, 'tags'),
    (r'^tags/(?P<tag>[^/]+)/$', PostTaggedList.as_view(), None, 'tagged'),
)

