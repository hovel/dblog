from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _

from django.views import generic

from dblog.models import Post, Blog
from dblog.forms import *

class BlogDetail(generic.DetailView):
    model = Blog

class BlogList(generic.ListView):
    model = Blog
    paginated_by = 30

class BlogUpdate(generic.UpdateView):
    model = Blog
    form_class = BlogForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BlogUpdate, self).dispatch(*args, **kwargs)

    def get_object(self, *args, **kwargs):
        self.object = super(BlogUpdate, self).get_object(*args, **kwargs)
        if not self.object.author == self.request.user or \
            not self.request.user.has_perm('dblog.can_manage'):
            raise Http404
        return self.object


class BlogPostList(generic.ListView):
    paginated_by = 30

    def get_queryset(self):
        self.blog = get_object_or_404(Blog, id=self.kwargs.get('pk'))
        queryset = Post.objects.filter(author=self.blog.author, is_draft=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(BlogPostList, self).get_context_data(**kwargs)
        context['blog'] = self.blog
        context['title'] = self.blog.title
        return context

class BlogPostDraftsList(generic.ListView):
    paginated_by = 30

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BlogPostDraftsList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.blog = get_object_or_404(Blog, id=self.kwargs.get('pk'))
        if not self.blog.author == self.request.user or \
            not self.request.user.has_perm('dblog.view_draft_posts'):
            raise Http404
        queryset = Post.objects.filter(author=self.blog.author, is_draft=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(BlogPostDraftsList, self).get_context_data(**kwargs)
        context['blog'] = self.blog
        context['title'] = ''.join([self.blog.title, ' (', _('Drafts'), ')'])
        return context

class PostList(generic.ListView):
    queryset = Post.objects.filter(is_draft=False)
    paginated_by = 30

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['title'] = _('Posts')
        return context

class PostDraftsList(generic.ListView):
    queryset = Post.objects.filter(is_draft=True)
    paginated_by = 30

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not request.user.has_perm('dblog.view_draft_posts'):
            return Http404
        return super(PostDraftsList, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['title'] = _('Draft posts')
        return context

class PostDetail(generic.DetailView):
    model = Post

class PostCreate(generic.CreateView):
    model = Post
    form_class = PostForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PostCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class PostUpdate(generic.UpdateView):
    model = Post
    form_class = PostForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PostUpdate, self).dispatch(*args, **kwargs)

    def get_object(self, *args, **kwargs):
        self.object = super(PostUpdate, self).get_object(*args, **kwargs)
        if not self.object.author == self.request.user:
            raise Http404
        return self.object

class PostDelete(generic.DeleteView):
    model = Post

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PostDelete, self).dispatch(*args, **kwargs)

class PostManage(generic.UpdateView):
    model = Post
    form_class = PostManageForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.has_perm('dblog.manage_post'):
            raise Http404
        return super(PostManage, self).dispatch(*args, **kwargs)

