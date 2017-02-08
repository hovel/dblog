from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'testproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^blogs/', include('dblog.urls.blog', namespace='blog')),
    url(r'^blog/', include('dblog.urls.post', namespace='post')),
]
