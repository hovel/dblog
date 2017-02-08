# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import tagging.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Your blog name.', max_length=64, verbose_name='Title')),
                ('author', models.OneToOneField(verbose_name='Author', to=settings.AUTH_USER_MODEL, help_text='Author association.')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Displayed on the browser tab and in the beginning of the article.', max_length=64, verbose_name='Title')),
                ('body', models.TextField(verbose_name='Body')),
                ('body_html', models.TextField(help_text='Ready to display text on the page.', verbose_name='Body HTML')),
                ('tags', tagging.fields.TagField(help_text='Comma separated tags.', max_length=255, verbose_name='Tags', blank=True)),
                ('created', models.DateTimeField(help_text='Created time.', verbose_name='Created', auto_now_add=True)),
                ('changed', models.DateTimeField(help_text='Changed time.', verbose_name='Changed', auto_now=True)),
                ('is_draft', models.BooleanField(default=True, help_text='After publishing, you can not make a post draft.', verbose_name='Is draft')),
                ('is_promoted', models.BooleanField(default=False, help_text='Publish this post on front page.', verbose_name='Is promoted')),
                ('enable_comments', models.BooleanField(default=True, help_text='Allow user to post comments.', verbose_name='Enable comments')),
                ('author', models.ForeignKey(related_name='blog_posts', verbose_name='Author', to=settings.AUTH_USER_MODEL, help_text='Author association.')),
                ('blog', models.ForeignKey(blank=True, to='dblog.Blog', help_text='Blog association.', null=True, verbose_name='Blog')),
            ],
            options={
                'ordering': ['-created'],
                'permissions': (('manage_post', 'Can manage post'),),
            },
        ),
    ]
