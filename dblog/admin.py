from django.contrib import admin
from dblog.models import Blog, Post


class PostInlineAdmin(admin.StackedInline):
    model = Post


class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title')
    inlines = (PostInlineAdmin,)
    max_num = 10


admin.site.register(Blog, BlogAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'changed')


admin.site.register(Post, PostAdmin)
