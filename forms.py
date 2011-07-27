from django import forms

from dblog.models import Blog, Post

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'is_draft', )

class PostDeleteForm(forms.Form):
    pass

class PostPromoteForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'is_draft', 'is_promoted',)
