from django import forms

from dblog.models import Blog, Post

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'is_draft', 'enable_comments', )

class PostPromotedForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'enable_comments', )

class PostDeleteForm(forms.Form):
    pass

class PostManageForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'body_html',)
