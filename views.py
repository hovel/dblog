from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, Http404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from django.views import generic

from dblog.models import Blog, Post
from dblog.forms import BlogForm, PostForm, PostDeleteForm, PostPromoteForm

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
        return super(PostCreate, self).dispatch(*args, **kwargs)

class PostList(generic.ListView):
    queryset = Post.objects.filter(is_draft=False)
    paginated_by = 30

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

class PostDelete(generic.DeleteView):
    model = Post

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PostDelete, self).dispatch(*args, **kwargs)

class PostPromote(generic.UpdateView):
    model = Post
    form_class = PostPromoteForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PostPromote, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.is_promoted = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class PostDemote(generic.UpdateView):
    model = Post

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PostDemote, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.is_promoted = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

