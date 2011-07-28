from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, Http404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

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

class PostManage(PostUpdate):
    form_class = PostManageForm