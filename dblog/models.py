from django.conf import settings
from django.contrib.auth.models import User
from django_comments.moderation import CommentModerator, moderator
from django_comments.models import Comment
import mptt
from django.contrib.sites.models import Site
from django.core.mail import mail_managers, send_mail
from django.db import models
from django.template import Context, loader
from django.utils.translation import ugettext as _

from tagging.fields import TagField
from tagging.models import Tag
from defaults import DBLOG_BODY_RENDER


class Blog(models.Model):
    author = models.OneToOneField('auth.User', verbose_name=_('Author'),
                                  help_text=_('Author association.'))
    title = models.CharField(max_length=64, verbose_name=_('Title'),
                             help_text=_('Your blog name.'))

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'blog:detail', [str(self.id), ]


class Post(models.Model):
    author = models.ForeignKey('auth.User', verbose_name=_('Author'),
                               help_text=_('Author association.'), related_name='blog_posts')
    blog = models.ForeignKey(Blog, blank=True, null=True, verbose_name=_('Blog'),
                             help_text=_('Blog association.'))
    title = models.CharField(max_length=64, verbose_name=_('Title'),
                             help_text=_('Displayed on the browser tab and in the beginning of the article.'))
    body = models.TextField(verbose_name=_('Body'))
    body_html = models.TextField(verbose_name=_('Body HTML'),
                                 help_text=_('Ready to display text on the page.'))
    tags = TagField(verbose_name=_('Tags'),
                    help_text=_('Comma separated tags.'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'),
                                   help_text=_('Created time.'))
    changed = models.DateTimeField(auto_now=True, verbose_name=_('Changed'),
                                   help_text=_('Changed time.'))
    is_draft = models.BooleanField(default=True, verbose_name=_('Is draft'),
                                   help_text=_('After publishing, you can not make a post draft.'))
    is_promoted = models.BooleanField(default=False, verbose_name=_('Is promoted'),
                                      help_text=_('Publish this post on front page.'))
    enable_comments = models.BooleanField(default=True,
                                          verbose_name=_('Enable comments'),
                                          help_text=_('Allow user to post comments.'))

    class Meta(object):
        ordering = ['-created', ]
        permissions = (
            ('manage_post', 'Can manage post'),
        )

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'post:detail', [str(self.id), ]

    def save(self, *args, **kwargs):
        self.body_html = DBLOG_BODY_RENDER(self.body)
        super(Post, self).save(*args, **kwargs)

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self):
        return Tag.objects.get_for_object(self)


class PostModerator(CommentModerator):
    email_notification = True
    enable_field = 'enable_comments'

    def email(self, comment, content_object, request):
        if self.email_notification:
            recipient = [content_object.author.email, ]
            site = Site.objects.get_current()
            t = loader.get_template('dblog/comments/comment_notification_email.txt')
            c = Context({'comment': comment,
                         'site': site,
                         'content_object': content_object})
            subject = '[%s] %s "%s"' % (site.name,
                                        _('New comment posted on'), content_object)
            message = t.render(c)
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                      recipient, fail_silently=True)

    def moderate(self, comment, content_object, request):
        if request.user.is_authenticated():
            return False
        return True

# Comments moderation
moderator.register(Post, PostModerator)

# Create a blog for every new user
def create_blog(sender, instance, created, *args, **kwargs):
    if created:
        title = instance.username + '\'s ' + _('blog')
        blog = Blog(author=instance, title=title)
        blog.save()


models.signals.post_save.connect(create_blog, sender=User)

# Notify managaers when user post published
def post_notify_managers(sender, instance, created, *args, **kwars):
    if not instance.is_draft:
        recipients = settings.MANAGERS
        site = Site.objects.get_current()
        subject = '[%s] %s: "%s"' % (site.name,
                                     _('New post published'), instance)
        t = loader.get_template('dblog/post_notification_email.txt')
        c = Context({'instance': instance,
                     'site': site})
        message = t.render(c)
        mail_managers(subject, message, fail_silently=True)


models.signals.post_save.connect(post_notify_managers, sender=Post)

