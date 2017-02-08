from django import template
from django_comments.models import Comment
from django.contrib.contenttypes.models import ContentType

from dblog.models import Post

register = template.Library()


@register.inclusion_tag('dblog/last_promoted.html')
def last_promoted(count):
    count = int(count)
    posts = Post.objects.filter(is_draft=False, is_promoted=True)[:count]
    return {'posts': posts}


@register.inclusion_tag('dblog/last_posts.html')
def last_posts(count):
    count = int(count)
    posts = Post.objects.filter(is_draft=False)[:count]
    return {'posts': posts}


@register.inclusion_tag('dblog/last_user_posts.html')
def last_user_posts(count, user):
    count = int(count)
    posts = Post.objects.filter(author=user,
                                is_draft=False)[:count]
    return {'posts': posts}


@register.inclusion_tag('dblog/last_comments.html')
def last_comments(count):
    count = int(count)
    content_type = ContentType.objects.get(app_label='dblog', model='post')
    comments = Comment.objects.filter(content_type=content_type,
                                      is_public=True, is_removed=False).order_by('-submit_date')[:count]
    return {'comments': comments}


@register.inclusion_tag('dblog/last_comments.html')
def last_user_comments(count, user):
    count = int(count)
    content_type = ContentType.objects.get(app_label='dblog', model='post')
    comments = Comment.objects.filter(content_type=content_type,
                                      is_public=True, is_removed=False, user=user).order_by('-submit_date')[:count]
    return {'comments': comments}
