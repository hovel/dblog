from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from markdown import markdown
import tagging

class Blog(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=64, verbose_name=_('Title'))

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blog:detail', [str(self.id), ])

class Post(models.Model):
    author = models.ForeignKey('auth.User', verbose_name=_('Author'))
    title = models.CharField(max_length=64, verbose_name=_('Title'))
    body = models.TextField(verbose_name=_('Body'))
    body_html = models.TextField(verbose_name=_('Body HTML'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    changed = models.DateTimeField(auto_now=True, verbose_name=_('Changed'))
    is_draft = models.BooleanField(default=True, verbose_name=_('Is draft'))
    is_promote = models.BooleanField(default=False, verbose_name=_('Is promoted'))

    class Meta:
        ordering = ['-created',]

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('post:detail', [str(self.id),])

    def save(self, *args, **kwargs):
        self.body_html = markdown(self.body, safe_mode='remove')
        super(Post, self).save(*args, **kwargs)

tagging.register(Post)

def create_blog(sender, instance, created, *args, **kwargs):
    if created:
        blog = Blog(author=instance, title=_('My blog'))
        blog.save()

models.signals.post_save.connect(create_blog, sender=User)
