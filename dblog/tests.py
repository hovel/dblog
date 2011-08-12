from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from dblog.models import Blog, Post
from dblog.forms import *


class BlogTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'test@test.test', 'user')
        self.another_user = User.objects.create_user('another',
            'another@test.test', 'another')
        self.manager_user = User.objects.create_user('manager',
            'manager@test.test', 'manager')
        permission = Permission.objects.get(codename='change_blog')
        self.manager_user.user_permissions.add(permission)
        
    def test_creation(self):
        blog = self.user.blog
        self.assertEqual(blog.title, self.user.username + '\'s blog')
        self.assertEqual(blog.author, self.user)

    def test_anonymous_views(self):
        client = Client()
        
        url = reverse('blog:detail', args=[self.user.blog.id])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['blog'], self.user.blog)
        self.assertEqual(response.context['title'], self.user.blog.title)
        
        url = reverse('blog:list')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 3)
        self.assertFalse(response.context['is_paginated'])

        url = reverse('blog:update', args=[self.user.blog.id])
        response = client.get(url)
        self.assertEqual(response.status_code, 302)
        response = client.post(url, {'title': 'Anon title'})
        self.assertEqual(response.status_code, 302)
        
        url = reverse('blog:drafts', args=[self.user.blog.id])
        response = client.get(url)
        self.assertEqual(response.status_code, 302)
        
    def test_another_user_views(self):
        client = Client()
        client.login(username='another', password='another')
        
        url = reverse('blog:detail', args=[self.user.blog.id])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['blog'], self.user.blog)
        self.assertEqual(response.context['title'], self.user.blog.title)
        
        url = reverse('blog:list')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        
        url = reverse('blog:update', args=[self.user.blog.id])
        response = client.get(url)
        self.assertEqual(response.status_code, 404)
        response = client.post(url, {'title': 'Another title'})
        self.assertEqual(response.status_code, 404)

        url = reverse('blog:drafts', args=[self.user.blog.id])
        response = client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_user_views(self):
        client = Client()
        client.login(username='user', password='user')

        url = reverse('blog:detail', args=[self.user.blog.id])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['blog'], self.user.blog)
        self.assertEqual(response.context['title'], self.user.blog.title)

        url = reverse('blog:list')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 3)
        self.assertFalse(response.context['is_paginated'])

        url = reverse('blog:update', args=[self.user.blog.id])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        response = client.post(url, {'title': 'New title'})
        self.assertRedirects(response, reverse('blog:detail',
            args=[self.user.blog.id]))

        url = reverse('blog:drafts', args=[self.user.blog.id])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 0)
        self.assertFalse(response.context['is_paginated'])

    def test_manages_views(self):
        client = Client()
        client.login(username='manager', password='manager')

        url = reverse('blog:detail', args=[self.user.blog.id])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['blog'], self.user.blog)
        self.assertEqual(response.context['title'], self.user.blog.title)

        url = reverse('blog:list')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 3)
        self.assertFalse(response.context['is_paginated'])

        url = reverse('blog:update', args=[self.user.blog.id])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        response = client.post(url, {'title': 'New title'})
        self.assertRedirects(response, reverse('blog:detail',
            args=[self.user.blog.id]))

        url = reverse('blog:drafts', args=[self.user.blog.id])
        response = client.get(url)
        self.assertEqual(response.status_code, 404)

class PostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@test.test', 'user')
        self.another_user = User.objects.create_user('another',
            'another@test.test', 'another')
        self.manager_user = User.objects.create_user('manager',
            'manager@test.test', 'manager')
        #permission = Permission.objects.get(codename='change_blog')
        #self.manager_user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='change_post')
        self.manager_user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='delete_post')
        self.manager_user.user_permissions.add(permission)
        self.blog = self.user.blog
        self.post = Post.objects.create(author=self.user, blog=self.blog,
            title='My title', body='My *body*.', tags='tag')

    def test_creation(self):
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.blog, self.blog)
        self.assertEqual(self.post.title, 'My title')
        self.assertEqual(self.post.body, 'My *body*.')
        self.assertEqual(self.post.body_html, '<p>My <em>body</em>.</p>')
        self.assertTrue(self.post.is_draft)
        self.assertFalse(self.post.is_promoted)
        self.assertTrue(self.post.enable_comments)

    def test_anonymous_views(self):
        client = Client()
        
        url = reverse('post:promoted')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 0)
        self.assertFalse(response.context['is_paginated'])

        url = reverse('post:feed')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('post:detail', args=[self.post.id,])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], self.post)

        url = reverse('post:create')
        response = client.get(url)
        self.assertEqual(response.status_code, 302)
        response = client.post(url, {'title': 'Anon title', 'body': 'Anon body'})
        self.assertEqual(response.status_code, 302)
        
        url = reverse('post:update', args=[self.post.id,])
        response = client.get(url)
        self.assertEqual(response.status_code, 302)
        response = client.post(url, {'title': 'Anon title'})
        self.assertEqual(response.status_code, 302)

        url = reverse('post:manage', args=[self.post.id,])
        response = client.get(url)
        self.assertEqual(response.status_code, 302)
        response = client.post(url)
        self.assertEqual(response.status_code, 302)
        
        url = reverse('post:delete', args=[self.post.id,])
        response = client.get(url)
        self.assertEqual(response.status_code, 302)
        response = client.post(url)
        self.assertEqual(response.status_code, 302)

        url = reverse('post:tags')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('post:tagged', args=['tag'])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_another_user_views(self):
        client = Client()
        client.login(username='another', password='another')

        url = reverse('post:promoted')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 0)
        self.assertFalse(response.context['is_paginated'])

        url = reverse('post:feed')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('post:detail', args=[self.post.id,])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], self.post)

        url = reverse('post:create')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        response = client.post(url, {'title': 'Another title', 'body': 'Anon body'})
        self.assertEqual(response.status_code, 302)

        url = reverse('post:update', args=[self.post.id,])
        response = client.get(url)
        self.assertEqual(response.status_code, 404)
        response = client.post(url, {'title': 'Another title'})
        self.assertEqual(response.status_code, 404)

        url = reverse('post:manage', args=[self.post.id,])
        response = client.get(url)
        self.assertEqual(response.status_code, 404)
        response = client.post(url, {'title': 'Another title'})
        self.assertEqual(response.status_code, 404)

        url = reverse('post:delete', args=[self.post.id,])
        response = client.get(url)
        self.assertEqual(response.status_code, 404)
        response = client.post(url, {'title': 'Another title'})
        self.assertEqual(response.status_code, 404)

        url = reverse('post:tags')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('post:tagged', args=['tag'])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_views(self):
        client = Client()
        client.login(username='user', password='user')

        url = reverse('post:promoted')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 0)
        self.assertFalse(response.context['is_paginated'])

        url = reverse('post:feed')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('post:detail', args=[self.post.id,])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], self.post)

        url = reverse('post:create')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        response = client.post(url, {'title': 'New title', 'body': 'New body'})
        self.assertEqual(response.status_code, 302)

        url = reverse('post:update', args=[self.post.id,])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        response = client.post(url, {'title': 'New title'})
        self.assertEqual(response.status_code, 200)

        url = reverse('post:manage', args=[self.post.id,])
        response = client.get(url)
        self.assertEqual(response.status_code, 404)
        response = client.post(url, {'title': 'Another title'})
        self.assertEqual(response.status_code, 404)

        url = reverse('post:delete', args=[self.post.id,])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        response = client.post(url)
        self.assertEqual(response.status_code, 302)

        url = reverse('post:tags')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('post:tagged', args=['tag'])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_manager_views(self):
        client = Client()
        client.login(username='manager', password='manager')

        url = reverse('post:promoted')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 0)
        self.assertFalse(response.context['is_paginated'])

        url = reverse('post:feed')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('post:detail', args=[self.post.id,])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], self.post)

        url = reverse('post:create')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        response = client.post(url, {'title': 'Manager title', 'body': 'Manager body'})
        self.assertEqual(response.status_code, 302)

        url = reverse('post:update', args=[self.post.id,])
        response = client.get(url)
        self.assertEqual(response.status_code, 404)
        response = client.post(url)
        self.assertEqual(response.status_code, 404)

        url = reverse('post:manage', args=[self.post.id,])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        response = client.post(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('post:delete', args=[self.post.id,])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        response = client.post(url)
        self.assertEqual(response.status_code, 302)

        url = reverse('post:tags')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('post:tagged', args=['tag'])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
