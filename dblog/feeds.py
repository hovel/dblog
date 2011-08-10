from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from dblog.models import Post

class LatestPostsFeed(Feed):
    title = _('Latest published posts')
    link = '/'
    description = _('New publications are always with you.')

    def items(self):
        return Post.objects.filter(is_draft=False, is_promoted=True)[:30]

    def item_tite(self, item):
        return item.title

    def item_description(self, item):
        return item.body_html