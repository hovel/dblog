from django.contrib import admin
from dblog.models import Blog, Post

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
admin.site.register(Blog, BlogAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'changed')
admin.site.register(Post, PostAdmin)
