from django import template
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType

from dblog.models import Post

register = template.Library()

@register.inclusion_tag('dblog/last_promoted.html')
def last_promoted(count):
    count = int(count)
    posts = Post.objects.filter(is_draft=False, is_promoted=True)[:count]
    return {'posts': posts}

@register.inclusion_tag('dblog/last_user_posts.html')
def last_user_posts(count, user):
    count = int(count)
    posts = Post.objects.filter(author=user,
        is_draft=False, is_promoted=True)[:count]
    return {'posts': posts}


@register.inclusion_tag('dblog/last_comments.html')
def last_comments(count=5):
    count = int(count)
    content_type = ContentType.objects.get(app_label='dblog', model='post')
    comments = Comment.objects.filter(content_type=content_type,
        is_public=True, is_removed=False)[:count]
    return {'comments':comments}
   